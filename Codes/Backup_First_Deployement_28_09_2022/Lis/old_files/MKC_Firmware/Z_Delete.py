from email import message
from azure.iot.device import IoTHubDeviceClient, Message
Iot_Connection_String = "HostName=mkc-iot-hub.azure-devices.net;DeviceId=sensors_001;SharedAccessKey=rEp4wNLKN/WybUfQLhLmiWmzcpga68RIGO2nTudNeYU="
from General_Configurations import Sensor_Configuration_File
import json
from datetime import datetime
import pytz
from Device_Communication import Device_Reading
import ast




# cod = COD_Reading()
# print(cod)



# def Azure_Read():
#         azure_input = str(input("Enter the message: "))
#         Command_Type = azure_input[0]
#         Control_Flag = azure_input[1]
#         Total_Length = int(azure_input[2:10], 16)
#         Variable_Length = int(azure_input[10:18], 16)
#         Topic_Name = azure_input[18: 18 + Variable_Length]
#         Message_Length = int(
#             azure_input[18 + Variable_Length: 26 + Variable_Length], 16)
#         Message_Content = azure_input[26 + Variable_Length:]

#         if Total_Length == (Variable_Length + Message_Length + 16):
#             receive_data = ast.literal_eval(Message_Content)
#             print(type(receive_data))
#             return receive_data
#         else:
#             print("The message is not being received appropriately.")

# Azure_Read()

def Configuration_Rewrite( variable, value):
        '''
        Description:
        Input Parameters:
        Output Type:

        '''
        with open(Sensor_Configuration_File, 'r') as file:
            json_data = json.load(file)
            json_data[variable] = value
            print(json_data[variable])
        with open(Sensor_Configuration_File, 'w') as file:
            json.dump(json_data, file)

data = "{'Time': 15, 'Energymeter': [171, 1, 46], 'COD': [101, 9729, 10], 'BOD': [101, 9729, 10], 'Temperature': [101, 9729, 10], 'TSS': [101, 4608, 4], 'Ph': [110, 9729, 5], 'TDS': [120, 9729, 4]}"
def Setting_Frequency_Time(data):
        azure_data = ast.literal_eval(data)
        if "Time" in azure_data:
            New_Frequency_Time = str(float(azure_data["Time"]))
            Configuration_Rewrite("Frequency_Time", New_Frequency_Time)
            return New_Frequency_Time
        else:
            print("No change in time")

Setting_Frequency_Time(data)


# def Adding_Sensor_Configuration(self,data):
#         '''
#         Description:
#         Input Parameters:
#         Output Type:
#         '''
#         azure_data = ast.literal_eval(data)
#         if "Energymeter" in azure_data:
#             self.Configuration_Add_Sensor_Details(azure_data, "Energymeter")
#         if "COD" in azure_data:
#             self.Configuration_Add_Sensor_Details(azure_data, "COD")
#         if "BOD" in azure_data:
#             self.Configuration_Add_Sensor_Details(azure_data, "BOD")
#         if "Temperature" in azure_data:
#             self.Configuration_Add_Sensor_Details(azure_data, "Temperature")
#         if "TSS" in azure_data:
#             self.Configuration_Add_Sensor_Details(azure_data, "TSS")
#         if "Ph" in azure_data:
#             self.Configuration_Add_Sensor_Details(azure_data, "TSS")
#         if "TDS" in azure_data:
# #             self.Configuration_Add_Sensor_Details(azure_data, "TSS")
from pymodbus.client.sync import ModbusTcpClient
# from General_Configurations import Gateway_Ip_Address, Gateway_Port, Sensor_Configuration_File


def Gateway_Connect():
    gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
    gateway_client.connect()
    print(gateway_client)
    print(type(gateway_client))
    return gateway_client

# Gateway_Connect()

# from General_Configurations import Gateway_Ip_Address, Gateway_Port, Sensor_Configuration_File
# from General_Configurations import Modbus_Error_Message, Modbus_Error, Modbus_Slave_Id_Error_Message, Modbus_Slave_Id_Error, Power_Error_Message, Power_Error
# def Gateway_Connect():
#         '''
#         Description:        To connect with the gateway client
#         Input Parameters:   None
#         Output Type:        pymodbus.client.sync.ModbusTcpClient
#         '''
#         gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
#         gateway_client.connect()
#         return gateway_client

def Get_Sensor_Reading(sensor):
        '''
        Description:        
        Input Parameters:   Sensor whose output is required
        Output Type:        pymodbus.client.sync.ModbusTcpClient
        '''
        sensor_result = []
        Connection_Checking_Count = 0
        sensor_config = "{}_Configurations".format(sensor)
        with open(Sensor_Configuration_File, 'r') as file:
            data = json.load(file)
        if sensor_config in data:
            sensor_configurations = data[sensor_config]
            for i in range(len(sensor_configurations)):
                sensor_details = {"{}_Device_Id".format(
                    sensor): sensor_configurations[i]["Device_ID"]}
                while True:
                    Sensor_Reading = Gateway_Connect().read_holding_registers(
                        count=sensor_configurations[i]["Register_Counts"], address=sensor_configurations[i]["Start_Address"], unit=sensor_configurations[i]["Device_ID"])
                    Sensor_Reading_check = str(Sensor_Reading)

                    if Sensor_Reading_check == Modbus_Error_Message:
                        Connection_Checking_Count = Connection_Checking_Count+1
                        if Connection_Checking_Count == 10:
                            sensor_result.append(sensor_details | Modbus_Error)
                            break

                    elif Sensor_Reading_check == Modbus_Slave_Id_Error_Message:
                        sensor_result.append(
                            sensor_details | Modbus_Slave_Id_Error)
                        break

                    elif Sensor_Reading_check == Power_Error_Message:
                        sensor_result.append(sensor_details | Power_Error)
                        break

                    else:
                        sensor_result.append(Sensor_Reading.registers)
                        break
            return sensor_result



# a=Get_Sensor_Reading("COD")
# print(a)
# a = Device_Reading().Get_Sensor_Reading("COD")
# print(a)


def Read_Frequency():
        with open(Sensor_Configuration_File, "r") as file:
            file_data = json.load(file)
            frequency = file_data["Frequency_Time"]
            print(type(frequency))
            print(frequency)
            return frequency



Read_Frequency()