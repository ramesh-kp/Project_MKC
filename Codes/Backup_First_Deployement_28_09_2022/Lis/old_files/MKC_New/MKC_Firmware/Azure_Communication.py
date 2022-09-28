from re import A
from azure.iot.device import IoTHubDeviceClient, Message
import struct
import pytz
from datetime import datetime, timedelta
import json
import ast

from Device_Communication import Device_Reading
from Logging_Info import Data_Logs
from General_Configurations import Sending_Iot_Connection_String, Receiving_Iot_Connection_String, Network_Connection_Error, Ethernet_Network_Error, Variable_Header, Command_Type
from General_Configurations import Sensor_Configuration_File, Validation_Error


result = {}


class Send_Sensor_Datas:
    __instance = None

    @staticmethod
    def getInstance():
        if Send_Sensor_Datas.__instance == None:
            Send_Sensor_Datas()
        return Send_Sensor_Datas.__instance

    def __init__(self):
        try:
            self.iothub_client = IoTHubDeviceClient.create_from_connection_string(
                Sending_Iot_Connection_String)
            if Send_Sensor_Datas.__instance != None:
                raise Exception("This class is a singleton!")
            else:
                Send_Sensor_Datas.__instance = self
        except ValueError:
            print("Invalid connection_string")
        except TypeError:
            print("Unsupported parameter")

    def Read_Frequency(self):
        '''
        Description:        Returns the Frequency_Time in Sensor_Configuration_File.
        Input Parameters:   None
        Output Type:        String
        '''
        try:
            with open(Sensor_Configuration_File, "r") as file:
                file_data = json.load(file)
                frequency = file_data["Frequency_Time"]
                if frequency in file_data.values():
                    print(type(frequency))
                    return frequency
                else:
                    return (Validation_Error["MKC1"])
        except Exception as e:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return (Validation_Error["MKC2"])

    # def Iothub_Client_Init(self):
    #     '''
    #     Description:        Instantiate the client from a IoTHub device or module connection string.
    #     Input Parameters:   None
    #     Output Type:        azure.iot.device
    #     '''
    #     # self.iothub_client = IoTHubDeviceClient.create_from_connection_string(
    #     #     Sending_Iot_Connection_String)
    #     # return iothub_client

    # @staticmethod
    def Iothub_Client_Telemetry_Sample_Run(self, reading):
        '''
        Description:        To send the relevant information to Iothub.
        Input Parameters:   Message needs to sent to Iothub.
        Output Type:        None

        '''
        try:
            message = Message(str(reading))
            print("Sending message: {}".format(message))
            self.iothub_client.send_message(message)
            print("Message successfully sent")

        except Exception as e:
            print(Network_Connection_Error)

    def Little_To_Big_Endian(self, data):
        '''
        Description:        Returns a new bytearray object in which every pair of neighbouring objects is reversed from the end,
                            initialized from a string of hex numbers.
        Input Parameters:   String containing hex numbers.
        Output Type:        String

        '''
        t = bytearray.fromhex(data)
        t.reverse()
        return ''.join(format(x, '02x') for x in t).upper()

    def Parse_Raw_Data(self, Raw_Data, Array_Pos_1, Array_Pos_2):
        '''
        Description:        Sensor reading at Array_Pos_1,Array_Pos_2 is convereted to hexadecimal format of length 4
                            the result is combined, converted to Bigindian Format, and then converted to decimal.
        Input Parameters:   Readings from a sensor whose output will be in Little Indian format.
        Output Type:        Decimal.

        '''
        List_1 = hex(Raw_Data[Array_Pos_1]).replace('0x', '').zfill(4)
        List_2 = hex(Raw_Data[Array_Pos_2]).replace('0x', '').zfill(4)
        First_Post_Hex = self.Little_To_Big_Endian(List_1 + List_2)
        Reading = round(struct.unpack(
            '!f', bytes.fromhex(First_Post_Hex))[0], 2)
        return Reading

    def Parse_Raw_Data_Energymeter(Energymeter_Reading_Raw):
        '''
        Description:        Returns Energymeter_Data from Energymeter readings.
                            The energymeter's output will be bigindian format
        Input Parameters:   Energymeter readings
        Output Type:        Dictionary

        '''
        Slave_Id = Energymeter_Reading_Raw[1]
        Ckwh = Energymeter_Reading_Raw[5]/1000
        Ckah = Energymeter_Reading_Raw[7]/1000
        Voltage = Energymeter_Reading_Raw[9]/10
        Power_Factor_Line_1 = Energymeter_Reading_Raw[33]/100
        Power_Factor_Line_2 = Energymeter_Reading_Raw[35]/100
        Power_Factor_Line_3 = Energymeter_Reading_Raw[37]/100
        Total_Power_Factor = Energymeter_Reading_Raw[43]/100
        Frequency = Energymeter_Reading_Raw[45]/10
        Energymeter_Data = {"Energymeter_Device_ID": Slave_Id, "Energymeter_Ckwh": Ckwh, "Energymeter_Ckah": Ckah, "Energymeter_Voltage": Voltage, "Energymeter_Power_Factor_Line_1": Power_Factor_Line_1,
                            "Energymeter_Power_Factor_Line_2": Power_Factor_Line_2, "Energymeter_Power_Factor_Line_3": Power_Factor_Line_3, "Energymeter_Total_Power_Factor": Total_Power_Factor, "Energymeter_Frequency": Frequency}
        return Energymeter_Data

    def Get_Sensor_Configurations(self, sensor):
        '''
        Description:        Returns the specified device configurations.
        Input Parameters:   Device information whose output is in LittleIndian format
        Output Type:        list

        '''
        try:
            sensor_config = "{}_Configurations".format(sensor)
            with open(Sensor_Configuration_File, 'r') as file:
                data = json.load(file)
            if sensor_config in data:
                sensor_configurations = data[sensor_config]
                return sensor_configurations
            else:
                return Validation_Error["MKC1"]
        except Exception as e:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return Validation_Error["MKC2"]

    class Read_Sensor_Datas:
        def Local_Time(self):
            '''
            Description:        converts a datetime object containing current date and time to different string formats.
            Input Parameters:   None
            Output Type:        List
            '''
            current_time = str(datetime.utcnow() + timedelta(minutes=330))
            time_stamp = {"Local Time": current_time}
            result.update(time_stamp)

        def Energymeter_Reading(self):
            '''
            Description:        When connected, the energymeter will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input Parameters:   None
            Output Type:        None
            '''
            try:
                energymeter_reading = Device_Reading().Get_Sensor_Reading("Energymeter")
                for i in range(len(energymeter_reading)):
                    if isinstance(energymeter_reading[i], list):
                        original_energymeter_reading = Send_Sensor_Datas.Parse_Raw_Data_Energymeter(
                            energymeter_reading[i])
                        result.update(original_energymeter_reading)
                    else:
                        result.update(energymeter_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def COD_Reading(self):
            '''
            Description:        When connected, the COD sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input Parameters:   None
            Output Type:        None
            '''
            try:
                cod_reading = Device_Reading().Get_Sensor_Reading("COD")
                for i in range(len(cod_reading)):
                    if isinstance(cod_reading[i], list):
                        cod_data = Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            cod_reading[i], 2, 3)
                        cod_config = Send_Sensor_Datas.getInstance().Get_Sensor_Configurations("COD")
                        cod_send_data = {
                            "COD_Device_Id": cod_config[i]["Device_ID"], "COD_Data": cod_data}
                        result.update(cod_send_data)
                    else:
                        result.update(cod_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def BOD_Reading(self):
            '''
            Description:        When connected, the BOD sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            '''
            try:
                bod_reading = Device_Reading().Get_Sensor_Reading("BOD")
                for i in range(len(bod_reading)):
                    if isinstance(bod_reading[i], list):
                        bod_data = Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            bod_reading[i], 4, 5)
                        bod_config = Send_Sensor_Datas.getInstance().Get_Sensor_Configurations("COD")
                        bod_send_data = {
                            "BOD_Device_Id": bod_config[i]["Device_ID"], "BOD_Data": bod_data}
                        result.update(bod_send_data)
                    else:
                        result.update(bod_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def TSS_Reading(self):
            '''
            Description:        When connected, the TSS sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            '''
            try:
                tss_reading = Device_Reading().Get_Sensor_Reading("TSS")
                for i in range(len(tss_reading)):
                    if isinstance(tss_reading[i], list):
                        tss_data = Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            tss_reading[i], 0, 1)
                        tss_config = Send_Sensor_Datas.getInstance().Get_Sensor_Configurations("TSS")
                        tss_send_data = {
                            "TSS_Device_Id": tss_config[i]["Device_ID"], "TSS_Data": tss_data}
                        result.update(tss_send_data)
                    else:
                        result.update(tss_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def Temperature_Reading(self):
            '''
            Description:        When connected, the Temperature sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            '''
            try:
                temperature_reading = Device_Reading().Get_Sensor_Reading("Temperature")
                for i in range(len(temperature_reading)):
                    if isinstance(temperature_reading[i], list):
                        temperature_data = Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            temperature_reading[i], 0, 1)
                        temperature_config = Send_Sensor_Datas().getInstance(
                        ).Get_Sensor_Configurations("Temperature")
                        temperature_send_data = {
                            "Temperature_Device_Id": temperature_config[i]["Device_ID"], "Temperature_Data": temperature_data}
                        result.update(temperature_send_data)
                    else:
                        result.update(temperature_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def Ph_Reading(self):
            '''
            Description:        When connected, the Ph sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            '''
            try:
                ph_reading = Device_Reading().Get_Sensor_Reading("Ph")
                for i in range(len(ph_reading)):
                    if isinstance(ph_reading[i], list):
                        ph_data = Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            ph_reading[i], 2, 3)
                        ph_config = Send_Sensor_Datas.getInstance().Get_Sensor_Configurations("Ph")
                        ph_send_data = {
                            "Ph_Device_Id": ph_config[i]["Device_ID"], "Ph_Data": ph_data}
                        result.update(ph_send_data)
                    else:
                        result.update(ph_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def TDS_Reading(self):
            '''
             Description:        When connected, the TDS sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            '''
            try:
                tds_reading = Device_Reading().Get_Sensor_Reading("TDS")
                for i in range(len(tds_reading)):
                    if isinstance(tds_reading[i], list):
                        tds_data = Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            tds_reading[i], 2, 3)
                        tds_config = Send_Sensor_Datas.getInstance().Get_Sensor_Configurations("TDS")
                        tds_send_data = {
                            "TDS_Device_Id": tds_config[i]["Device_ID"], "TDS_Data": tds_data}
                        result.update(tds_send_data)
                    else:
                        result.update(tds_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def Conductivity_Reading(self):
            '''
            Description:        When connected, the conductivity sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            '''
            try:
                conductivity_reading = Device_Reading().Get_Sensor_Reading("Conductivity")
                for i in range(len(conductivity_reading)):
                    if isinstance(conductivity_reading[i], list):
                        conductivity_data = (Send_Sensor_Datas.getInstance().Parse_Raw_Data(
                            conductivity_reading[i], 0, 1))/10
                        conductivity_config = Send_Sensor_Datas().getInstance(
                        ).Get_Sensor_Configurations("Conductivity")
                        conductivity_send_data = {
                            "Conductivity_Device_Id": conductivity_config[i]["Device_ID"], "Conductivity_Data": conductivity_data}
                        result.update(conductivity_send_data)
                    else:
                        result.update(conductivity_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def Mqtt_Message_Format(self, sensor_data):
            data = str(sensor_data)
            MQTT_Message = Variable_Header + \
                format(len(data), "08x") + str(data)
            Total_Length = format(len(MQTT_Message), "08x")
            final_message = Command_Type + Total_Length + MQTT_Message
            return final_message

        def Full_Sensor_Readings(self):
            '''
            Description:        The result that we obtain from the  Local_Time(),Energymeter_Reading(), COD_Reading(),BOD_Reading(), TSS_Reading(),
                                Temperature_Reading(),Ph_Reading(),TDS_Reading() Conductivity_Reading() are passed to the Mqtt_Message_Format() and its output stored in final_data,
                                which is passed to the Iothub_Client_Telemetry_Sample_Run().Finally the final_data is written to the Send_Data_Logs
            Input Parameters:   None
            Output Type:        String
            '''
            global result
            self.Local_Time()
            self.Energymeter_Reading()
            self.COD_Reading()
            self.BOD_Reading()
            self.TSS_Reading()
            self.Temperature_Reading()
            self.Ph_Reading()
            self.TDS_Reading()
            self.Conductivity_Reading()
            final_data = self.Mqtt_Message_Format(result)
            result = {}
            Send_Sensor_Datas.getInstance().Iothub_Client_Telemetry_Sample_Run(final_data)
            Data_Logs().Send_Data_Logs(final_data)


class Receive_Azure_Data(Send_Sensor_Datas):
    def __init__(self):
        self.getInstance()

    def Configuration_Rewrite(self, variable, value):
        '''
        Description:        read the Sensor_Configuration_File and overwrite the file with input time
        Input Parameters:   "Frequency_Time" and input time
        Output Type:        None
        '''
        try:
            with open(Sensor_Configuration_File, 'r') as file:
                json_data = json.load(file)
                if variable in json_data:
                    json_data[variable] = value
                else:
                    return Validation_Error["MKC1"]
            with open(Sensor_Configuration_File, 'w') as file:
                json.dump(json_data, file)
        except:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return Validation_Error["MKC2"]

    def Configuration_Add(self, sensor, value):
        '''
        Description:        read the Sensor_Configuration_File and append the file with configurations of newly added sensors.
        Input Parameters:   sensor name and the corresponding sensor datas
        Output Type:        None
        '''
        try:
            with open(Sensor_Configuration_File, 'r+') as file:
                file_data = json.load(file)
                if value not in file_data[sensor]:
                    file_data[sensor].append(value)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                else:
                    return Validation_Error["MKC3"]
        except:
            Data_Logs().Error_log("{},{}".format(
                sensor, Validation_Error["MKC2"]))
            return Validation_Error["MKC2"]

    def Configuration_Add_Sensor_Details(self, data, sensor):
        '''
        Description:        Add Sensor details to Sensor_Configuration_File from the data we get from Azure.
        Input Parameters:   Sensor and Corresponding details of the sensor
        Output Type:        None
        '''

        sensor_config = "{}_Configurations".format(sensor)
        length_key = len(data[sensor])
        if length_key == 3:
            New_Configuration = {}
            New_Configuration["Device_ID"] = data[sensor][0]
            New_Configuration["Start_Address"] = data[sensor][1]
            New_Configuration["Register_Counts"] = data[sensor][2]
            self.Configuration_Add(
                sensor_config, New_Configuration)
        else:
            Data_Logs().Error_log("{},{}".format(
                sensor, Validation_Error["MKC7"]))
            return Validation_Error["MKC7"]

    def Azure_Read(self):
        '''
        Description:        The input message is convereted to the data received from the sensors.
        Input Parameters:   None
        Output type:        Dictionary if message is received appropriately else a string.
        '''
        try:
            with open('Read_data.json', 'r') as file:
                data = json.load(file)
            for key in data.keys():
                azure_input = data[key]
            with open('Read_data.json', 'w') as file:
                json.dump([], file)

            print("Azure Input: ", azure_input)
            Command_Type = azure_input[0]
            Control_Flag = azure_input[1]
            Total_Length = int(azure_input[2:10], 16)
            Variable_Length = int(azure_input[10:18], 16)
            Topic_Name = azure_input[18: 18 + Variable_Length]
            print(Topic_Name)
            if Topic_Name == "MKC_WIRAS_SENSOR_DATA":
                Message_Length = int(
                    azure_input[18 + Variable_Length: 26 + Variable_Length], 16)
                Message_Content = azure_input[26 + Variable_Length:]
                Message_Content_length = len(
                    azure_input[26 + Variable_Length:])
                if Total_Length == (Variable_Length + Message_Length + 16):
                    if Message_Content_length == Message_Length:
                        receive_data = ast.literal_eval(Message_Content)
                        Data_Logs().Receive_Data_Logs(receive_data)
                        Send_Sensor_Datas().getInstance().Iothub_Client_Telemetry_Sample_Run(
                            receive_data)
                        return receive_data
                else:
                    print("The message is not being received appropriately.")
            else:
                print("Incorrect Topic name")
        except AttributeError:
            print("File is empty")
        except Exception as e:
            print(e)
            # Data_Logs().Error_log(Validation_Error["MKC5"])
            # return Validation_Error["MKC5"]

    def Setting_Frequency_Time(self, data):
        '''
        Description:        overwriting the time in Sensor_Configuration_File with that we get in the input data
        Input Parameters:   data retrieved from Azure
        Output Type:        None
        '''
        try:
            azure_data = ast.literal_eval(data)
            if "Time" in azure_data:
                New_Frequency_Time = str(float(azure_data["Time"]))
                self.Configuration_Rewrite(
                    "Frequency_Time", New_Frequency_Time)
                return New_Frequency_Time
            else:
                print("No change in time")
        except:
            Data_Logs().Error_log(Validation_Error["MKC6"])
            return Validation_Error["MKC6"]

    def Adding_Sensor_Configuration(self, data):
        '''
        Description:        Add Sensor details to Sensor_Configuration_File from the input data
        Input Parameters:   data retrieved from Azure
        Output Type:        None
        '''
        try:
            azure_data = ast.literal_eval(data)
            if "Energymeter" in azure_data:
                self.Configuration_Add_Sensor_Details(
                    azure_data, "Energymeter")
            if "COD" in azure_data:
                self.Configuration_Add_Sensor_Details(azure_data, "COD")
            if "BOD" in azure_data:
                self.Configuration_Add_Sensor_Details(azure_data, "BOD")
            if "Temperature" in azure_data:
                self.Configuration_Add_Sensor_Details(
                    azure_data, "Temperature")
            if "TSS" in azure_data:
                self.Configuration_Add_Sensor_Details(azure_data, "TSS")
            if "Ph" in azure_data:
                self.Configuration_Add_Sensor_Details(azure_data, "Ph")
            if "TDS" in azure_data:
                self.Configuration_Add_Sensor_Details(azure_data, "TDS")
            if "Conductivity" in azure_data:
                self.Configuration_Add_Sensor_Details(
                    azure_data, "Conductivity")
        except:
            Data_Logs().Error_log(Validation_Error["MKC6"])
            return Validation_Error["MKC6"]

    def Clear_Configuration(self, data):
        '''
        Description:        Clear data from Sensor_Configuration_File
        Input Parameters:   data retrieved from Azure
        Output Type:        None
        '''
        try:
            azure_data = ast.literal_eval(data)
            if "RESET" in azure_data:
                with open(Sensor_Configuration_File, 'r') as file:
                    json_data = json.load(file)
                    json_data["Frequency_Time"] = "0"
                    json_data["Energymeter_Configurations"].clear()
                    json_data["COD_Configurations"].clear()
                    json_data["BOD_Configurations"].clear()
                    json_data["Temperature_Configurations"].clear()
                    json_data["TSS_Configurations"].clear()
                    json_data["Ph_Configurations"].clear()
                    json_data["TDS_Configurations"].clear()
                    json_data["Conductivity_Configurations"].clear()
                with open(Sensor_Configuration_File, 'w') as file:
                    json.dump(json_data, file)
        except:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return Validation_Error["MKC2"]

    def Azure_data_Config():
        '''
        Description:        To Get the data that we receive from Azure
        Input Parameters:   None
        Output Type:        None
        '''
        print("jijiji")
        azure_data = str(Receive_Azure_Data().Azure_Read())
        Receive_Azure_Data().Setting_Frequency_Time(azure_data)
        Receive_Azure_Data().Adding_Sensor_Configuration(azure_data)
        Receive_Azure_Data().Clear_Configuration(azure_data)


# azure_data = str(Receive_Azure_Data().Azure_Read())
# Receive_Azure_Data().Setting_Frequency_Time(azure_data)
# Receive_Azure_Data().Adding_Sensor_Configuration(azure_data)
# Receive_Azure_Data().Clear_Configuration(azure_data)


# Receive_Azure_Data().Azure_data_Config()
# Receive_Azure_Data().Azure_Read()
