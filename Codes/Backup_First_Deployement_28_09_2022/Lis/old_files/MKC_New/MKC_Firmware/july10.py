from re import A
from azure.iot.device import IoTHubDeviceClient, Message
from azure.iot.device.exceptions import CredentialError, ConnectionFailedError, ConnectionDroppedError, ClientError, OperationTimeout, NoConnectionError
import struct
import pytz
from datetime import datetime, timedelta
import json
import ast
import glob

from Device_Communication import Device_Reading
from Logging_Info import Data_Logs
from General_Configurations import Sending_Iot_Connection_String, Receiving_Iot_Connection_String, Network_Connection_Error, Ethernet_Network_Error, Variable_Header, Command_Type
from General_Configurations import Sensor_Configuration_File, Validation_Error, Sensor_Reading_File


result = {}
file_number = 1


class Send_Sensor_Datas:

    def read_frequency(self):
        '''
        Description:        Returns the Frequency_Time in Sensor_Configuration_File.
        Input Parameters:   None
        Output Type:        String
        '''
        try:
            with open(Sensor_Configuration_File, "r") as file:
                sensor_configurations_data = json.load(file)
                frequency = sensor_configurations_data["Frequency_Time"]
                if frequency in sensor_configurations_data.values():
                    return frequency
                else:
                    return (Validation_Error["MKC1"])
        except FileNotFoundError:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return (Validation_Error["MKC2"])

    def iothub_client_telemetry_sample_run(self, iothub_client, reading):
        '''
        Description:        To send the relevant information to Iothub.
        Input Parameters:   Message needs to sent to Iothub.
        Output Type:        None

        '''
        try:
            message = Message(str(reading))
            print("Sending message: {}".format(message))
            iothub_client.send_message(message)
            print("Message successfully sent")

        except CredentialError:
            print("credentials are invalid and a connection cannot be established")
        except ConnectionFailedError:
            print("Establishing a connection results in failure")
        except ConnectionDroppedError:
            print("Connection is lost during execution")
        except OperationTimeout:
            print(" connection attempt times out")
        except NoConnectionError:
            print("Client is not connected")
        except ClientError:
            print("Unexpected failure during execution")

    def little_to_big_endian(self, input_str):
        '''
        Description:        Little Endian to Big Endian.Returns a new bytearray object in which every pair of neighbouring objects is reversed from the end,
                            initialized from a string of hex numbers.
        Input Parameters:   String containing hex numbers.
        Output Type:        String

        '''
        hex_string = bytearray.fromhex(input_str)
        hex_string.reverse()
        return ''.join(format(x, '02x') for x in hex_string).upper()

    def parse_raw_data(self, Raw_Data, Array_Pos_1, Array_Pos_2):
        '''
        Description:        Convert Raw Data to Real Value.Sensor reading at Array_Pos_1,Array_Pos_2 is convereted to hexadecimal format of length 4
                            the result is combined, converted to Bigindian Format, and then converted to decimal.
        Input Parameters:   Readings from a sensor whose output will be in Little Indian format.
        Output Type:        Decimal.

        '''
        List_1 = hex(Raw_Data[Array_Pos_1]).replace('0x', '').zfill(4)
        List_2 = hex(Raw_Data[Array_Pos_2]).replace('0x', '').zfill(4)
        First_Post_Hex = self.little_to_big_endian(List_1 + List_2)
        Reading = round(struct.unpack(
            '!f', bytes.fromhex(First_Post_Hex))[0], 2)
        return Reading

    def parse_raw_data_energymeter(Energymeter_Reading_Raw):
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

    def get_sensor_configurations(self, sensor):
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
        except FileNotFoundError:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return Validation_Error["MKC2"]

    class Read_Sensor_Datas:
        def local_time(self):
            '''
            Description:        converts a datetime object containing current date and time to different string formats.
            Input Parameters:   None
            Output Type:        List
            '''
            current_time = str(datetime.utcnow() + timedelta(minutes=330))
            time_stamp = {"Local Time": current_time}
            result.update(time_stamp)

        def energymeter_reading(self):
            """
            Description:        When connected, the energymeter will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input Parameters:   None
            Output Type:        None
            """
            try:
                energymeter_reading = Device_Reading().get_sensor_reading("Energymeter")
                for i in range(len(energymeter_reading)):
                    if isinstance(energymeter_reading[i], list):
                        original_energymeter_reading = Send_Sensor_Datas().parse_raw_data_energymeter(
                            energymeter_reading[i])
                        result.update(original_energymeter_reading)
                    else:
                        result.update(energymeter_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def COD_reading(self):
            """
            Description:        When connected, the COD sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input Parameters:   None
            Output Type:        None
            """
            try:
                cod_reading = Device_Reading().get_sensor_reading("COD")
                for i in range(len(cod_reading)):
                    if isinstance(cod_reading[i], list):
                        cod_data = Send_Sensor_Datas().parse_raw_data(
                            cod_reading[i], 2, 3)
                        cod_config = Send_Sensor_Datas().get_sensor_configurations("COD")
                        cod_send_data = {
                            "COD_Device_Id": cod_config[i]["Device_ID"], "COD_Data": cod_data}
                        result.update(cod_send_data)
                    else:
                        result.update(cod_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def BOD_reading(self):
            """
            Description:        When connected, the BOD sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            """
            try:
                bod_reading = Device_Reading().get_sensor_reading("BOD")
                for i in range(len(bod_reading)):
                    if isinstance(bod_reading[i], list):
                        bod_data = Send_Sensor_Datas().parse_raw_data(
                            bod_reading[i], 4, 5)
                        bod_config = Send_Sensor_Datas().get_sensor_configurations("COD")
                        bod_send_data = {
                            "BOD_Device_Id": bod_config[i]["Device_ID"], "BOD_Data": bod_data}
                        result.update(bod_send_data)
                    else:
                        result.update(bod_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def TSS_reading(self):
            """
            Description:        When connected, the TSS sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            """
            try:
                tss_reading = Device_Reading().get_sensor_reading("TSS")
                for i in range(len(tss_reading)):
                    if isinstance(tss_reading[i], list):
                        tss_data = Send_Sensor_Datas().parse_raw_data(
                            tss_reading[i], 0, 1)
                        tss_config = Send_Sensor_Datas().get_sensor_configurations("TSS")
                        tss_send_data = {
                            "TSS_Device_Id": tss_config[i]["Device_ID"], "TSS_Data": tss_data}
                        result.update(tss_send_data)
                    else:
                        result.update(tss_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def temperature_reading(self):
            """
            Description:        When connected, the Temperature sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            """
            try:
                temperature_reading = Device_Reading().get_sensor_reading("Temperature")
                for i in range(len(temperature_reading)):
                    if isinstance(temperature_reading[i], list):
                        temperature_data = Send_Sensor_Datas().parse_raw_data(
                            temperature_reading[i], 0, 1)
                        temperature_config = Send_Sensor_Datas(
                        ).get_sensor_configurations("Temperature")
                        temperature_send_data = {
                            "Temperature_Device_Id": temperature_config[i]["Device_ID"], "Temperature_Data": temperature_data}
                        result.update(temperature_send_data)
                    else:
                        result.update(temperature_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def Ph_reading(self):
            """
            Description:        When connected, the Ph sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            """
            try:
                ph_reading = Device_Reading().get_sensor_reading("Ph")
                for i in range(len(ph_reading)):
                    if isinstance(ph_reading[i], list):
                        ph_data = Send_Sensor_Datas().parse_raw_data(
                            ph_reading[i], 2, 3)
                        ph_config = Send_Sensor_Datas().get_sensor_configurations("Ph")
                        ph_send_data = {
                            "Ph_Device_Id": ph_config[i]["Device_ID"], "Ph_Data": ph_data}
                        result.update(ph_send_data)
                    else:
                        result.update(ph_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def TDS_reading(self):
            """
             Description:        When connected, the TDS sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            """
            try:
                tds_reading = Device_Reading().get_sensor_reading("TDS")
                for i in range(len(tds_reading)):
                    if isinstance(tds_reading[i], list):
                        tds_data = Send_Sensor_Datas().parse_raw_data(
                            tds_reading[i], 2, 3)
                        tds_config = Send_Sensor_Datas().get_sensor_configurations("TDS")
                        tds_send_data = {
                            "TDS_Device_Id": tds_config[i]["Device_ID"], "TDS_Data": tds_data}
                        result.update(tds_send_data)
                    else:
                        result.update(tds_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def conductivity_reading(self):
            """
            Description:        When connected, the conductivity sensor will deliver the output as a list; otherwise, it will be a dictionary.
                                Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
                                each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
                                the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
            Input parameters:   None
            Output type:        None
            """
            try:
                Conductivity_reading = Device_Reading().get_sensor_reading("Conductivity")
                for i in range(len(Conductivity_reading)):
                    if isinstance(Conductivity_reading[i], list):
                        conductivity_data = (Send_Sensor_Datas().parse_raw_data(
                            Conductivity_reading[i], 0, 1))/10
                        conductivity_config = Send_Sensor_Datas().get_sensor_configurations("Conductivity")
                        conductivity_send_data = {
                            "Conductivity_Device_Id": conductivity_config[i]["Device_ID"], "Conductivity_Data": conductivity_data}
                        result.update(conductivity_send_data)
                    else:
                        result.update(Conductivity_reading[i])
            except Exception as e:
                return Ethernet_Network_Error["Error_Message"]

        def mqtt_message_format(self, sensor_data):
            """
            Description:        Sensor reading combined with Variable_Header to converts it to Mqtt message.
            Input parameters:   Sensor readings
            Output type:        String
            """
            data = str(sensor_data)
            MQTT_Message = Variable_Header + \
                format(len(data), "08x") + str(data)
            Total_Length = format(len(MQTT_Message), "08x")
            final_message = Command_Type + Total_Length + MQTT_Message
            return final_message

        def latest_file_generated(self):
            """
            Description:        Return the Json file which generated currently.
            Input parameters:   None
            Output type:        Json file
            """
            try:
                json_files = sorted(glob.glob("*.json"))
                return str(json_files[-3])
            except FileNotFoundError:
                Data_Logs().Error_log(Validation_Error["MKC2"])
                return (Validation_Error["MKC2"])

        def first_file_generated(self):
            """
            Description:        Return the Json file which generated first.
            Input parameters:   None
            Output type:        Json file
            """
            try:
                json_files = sorted(glob.glob("*.json"))
                return str(json_files[2])
            except FileNotFoundError:
                Data_Logs().Error_log(Validation_Error["MKC2"])
                return (Validation_Error["MKC2"])

        def delete_sensor_readings(self, iotclient_obj):
            """
            Description:        Open the first file generated,once the sensor readings are send to azure the file is truncated.
            Input parameters:   None
            Output type:        None
            """
            try:
                first_file = self.first_file_generated()
                with open(first_file, 'r+') as file:
                    file_data = json.load(file)
                    final_data = self.mqtt_message_format(file_data)
                    result = Send_Sensor_Datas(
                    ).iothub_client_telemetry_sample_run(iotclient_obj, final_data)

                    if result == None:
                        first_key = int(list(file_data.keys())[0])
                        last_key = int(list(file_data.keys())[-1])
                        for i in range(int(first_key), int(last_key)):
                            file_data.pop(str(i))
                        file.truncate(0)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                        del file_data
            except FileNotFoundError:
                Data_Logs().Error_log(Validation_Error["MKC2"])
                return (Validation_Error["MKC2"])

        def send_sensor_readings_add(self, data):
            """
            Description:        Open the last file generated,add sensor readings to that file.Once the file reaches 2000 lines,a new file is created.
            Input parameters:   Sensor readings
            Output type:        None
            """
            global file_number
            latest_file = self.latest_file_generated()
            with open(latest_file, 'r+') as file:
                file_data = json.load(file)
                if file_data:
                    last_number = int(list(file_data.keys())[-1])
                    data = {last_number + 1: data}
                else:
                    last_number = 0
                    data = {last_number + 1: data}
                if last_number == 2001:
                    last_number = 1
                file_data.update(data)
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
                if len(file_data.keys()) == 2000:
                    with open('Sensor_Readings_{}.json'.format(file_number), 'w') as file:
                        file_number = file_number + 1
                        file.seek(0)
                        json.dump(data, file, indent=4)

        def full_sensor_readings(self, client_obj):
            '''
            Description:        The result that we obtain from the  Local_Time(),Energymeter_Reading(), COD_Reading(),BOD_Reading(), TSS_Reading(),
                                Temperature_Reading(),Ph_Reading(),TDS_Reading() conductivity_reading() are passed to the mqtt_message_format() and its output stored in final_data,
                                which saved to a json file.
            Input Parameters:   None
            Output Type:        String
            '''
            global result
            self.local_time()
            self.energymeter_reading()
            self.COD_reading()
            self.BOD_reading()
            self.TSS_reading()
            self.temperature_reading()
            self.Ph_reading()
            self.TDS_reading()
            self.conductivity_reading()
            self.send_sensor_readings_add(result)
            self.delete_sensor_readings(client_obj)
            result = {}


class Receive_Azure_Data:
    def __init__(self):
        pass
        # self.getInstance()

    def configuration_rewrite(self, variable, value):
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

    def configuration_add(self, sensor, value):
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

    def configuration_add_sensor_details(self, data, sensor):
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
            self.configuration_add(
                sensor_config, New_Configuration)
        else:
            Data_Logs().Error_log("{},{}".format(
                sensor, Validation_Error["MKC7"]))
            return Validation_Error["MKC7"]

    def azure_read(self, instobj):
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
                        print("instobj", instobj)
                        Data_Logs().Receive_Data_Logs(receive_data)
                        Send_Sensor_Datas().iothub_client_telemetry_sample_run(instobj,
                                                                               receive_data)
                        return receive_data
                else:
                    print("The message is not being received appropriately.")
            else:
                print("Incorrect Topic name")
        except AttributeError:
            Data_Logs().Error_log(Validation_Error["MKC8"])
            return (Validation_Error["MKC8"])
        except FileNotFoundError:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return (Validation_Error["MKC2"])
        except ValueError:
            Data_Logs().Error_log(Validation_Error["MKC5"])
            return Validation_Error["MKC5"]

    def setting_frequency_time(self, data):
        '''
        Description:        overwriting the time in Sensor_Configuration_File with that we get in the input data
        Input Parameters:   data retrieved from Azure
        Output Type:        None
        '''
        try:
            azure_data = ast.literal_eval(data)
            if "Time" in azure_data:
                New_Frequency_Time = str(float(azure_data["Time"]))
                self.configuration_rewrite(
                    "Frequency_Time", New_Frequency_Time)
                return New_Frequency_Time
            else:
                print("No change in time")
        except:
            Data_Logs().Error_log(Validation_Error["MKC6"])
            return Validation_Error["MKC6"]

    def adding_sensor_configuration(self, data):
        '''
        Description:        Add Sensor details to Sensor_Configuration_File from the input data
        Input Parameters:   data retrieved from Azure
        Output Type:        None
        '''
        try:
            azure_data = ast.literal_eval(data)
            if "Energymeter" in azure_data:
                self.configuration_add_sensor_details(
                    azure_data, "Energymeter")
            if "COD" in azure_data:
                self.configuration_add_sensor_details(azure_data, "COD")
            if "BOD" in azure_data:
                self.configuration_add_sensor_details(azure_data, "BOD")
            if "Temperature" in azure_data:
                self.configuration_add_sensor_details(
                    azure_data, "Temperature")
            if "TSS" in azure_data:
                self.configuration_add_sensor_details(azure_data, "TSS")
            if "Ph" in azure_data:
                self.configuration_add_sensor_details(azure_data, "Ph")
            if "TDS" in azure_data:
                self.configuration_add_sensor_details(azure_data, "TDS")
            if "Conductivity" in azure_data:
                self.configuration_add_sensor_details(
                    azure_data, "Conductivity")
        except:
            Data_Logs().Error_log(Validation_Error["MKC6"])
            return Validation_Error["MKC6"]

    def clear_configuration(self, data):
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

    def azure_data_config(client_obj):
        '''
        Description:        To Get the data that we receive from Azure
        Input Parameters:   None
        Output Type:        None
        '''
        azure_data = str(Receive_Azure_Data().azure_read(client_obj))
        Receive_Azure_Data().setting_frequency_time(azure_data)
        Receive_Azure_Data().adding_sensor_configuration(azure_data)
        Receive_Azure_Data().clear_configuration(azure_data)


# azure_data = str(Receive_Azure_Data().Azure_Read())
# Receive_Azure_Data().Setting_Frequency_Time(azure_data)
# Receive_Azure_Data().Adding_Sensor_Configuration(azure_data)
# Receive_Azure_Data().Clear_Configuration(azure_data)


# Receive_Azure_Data().Azure_data_Config()
# Receive_Azure_Data().Azure_Read()
