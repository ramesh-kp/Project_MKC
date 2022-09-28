# import struct
# from Device_Communication import Device_Reading
# result = {}
# Ethernet_Network_Error = {"Error_Message": "Error in Ethernet Network"}


# from pymodbus.client.sync import ModbusTcpClient

# from General_Configurations import Gateway_Ip_Address, Gateway_Port, Sensor_Configuration_File, Validation_Error
# from General_Configurations import Modbus_Error_Message, Modbus_Error, Modbus_Slave_Id_Error_Message, Modbus_Slave_Id_Error, Power_Error_Message, Power_Error
# from Logging_Info import Data_Logs
# import json

# class Send_Sensor_Datas:
#     def parse_raw_data(self, Raw_Data, Array_Pos_1, Array_Pos_2):
#         '''
#         Description:        Convert Raw Data to Real Value.Sensor reading at Array_Pos_1,Array_Pos_2 is convereted to hexadecimal format of length 4
#                             the result is combined, converted to Bigindian Format, and then converted to decimal.
#         Input Parameters:   Readings from a sensor whose output will be in Little Indian format.
#         Output Type:        Decimal.

#         '''
#         List_1 = hex(Raw_Data[Array_Pos_1]).replace('0x', '').zfill(4)
#         List_2 = hex(Raw_Data[Array_Pos_2]).replace('0x', '').zfill(4)
#         First_Post_Hex = self.little_to_big_endian(List_1 + List_2)
#         Reading = round(struct.unpack(
#             '!f', bytes.fromhex(First_Post_Hex))[0], 2)
#         return Reading


# def get_tds_reading():
#             '''
#              Description:        When connected, the TDS sensor will deliver the output as a list; otherwise, it will be a dictionary.
#                                 Each output is appended to a list,which is iterated over number of entries in the list.and  verify  whether
#                                 each element is a list. If the ontput is a list, a function will be called, based on the requirement few of
#                                 the index values are taken and form a dictionary.Those dictionaries are further appended to form a list.
#             Input parameters:   None
#             Output type:        None
#             '''
#             try:
#                 tds_reading = Device_Reading().get_sensor_reading("TDS")
#                 for i in range(len(tds_reading)):
#                     if isinstance(tds_reading[i], list):
#                         tds_data = Send_Sensor_Datas().parse_raw_data(
#                             tds_reading[i], 2, 3)
#                         tds_config = Send_Sensor_Datas().get_sensor_configurations("TDS")
#                         tds_send_data = {
#                             "TDS_Device_Id": tds_config[i]["Device_ID"], "TDS_Data": tds_data}
#                         result.update(tds_send_data)
#                     else:
#                         result.update(tds_reading[i])
#             except:
#                 return Ethernet_Network_Error["Error_Message"]

# class Device_Reading():
#     def gateway_connect(self):
#         '''
#         Description:        Establish connection of sensor with raspberry pi.
#         Input Parameters:   None
#         Output Type:        Object ModbusClient
#         '''
#         gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
#         gateway_client.connect()
#         return gateway_client

#     def get_sensor_reading(sensor):
#         '''
#         Description:        Returns sensor readings of the sensor given in the input parameter.
#         Input Parameters:   sensor configurations
#         Output Type:        sensor readings
#         '''
#         try:
#             sensor_result = []
#             Connection_Checking_Count = 0
#             sensor_config = "{}_Configurations".format(sensor)
#             with open(Sensor_Configuration_File, 'r') as file:
#                 data = json.load(file)
#             if sensor_config in data:
#                 sensor_configurations = data[sensor_config]
#                 for i in range(len(sensor_configurations)):
#                     sensor_details = {"{}_Device_Id".format(
#                         sensor): sensor_configurations[i]["Device_ID"]}
#                     while True:
#                         Sensor_Reading = gateway_connect().read_holding_registers(
#                             count=sensor_configurations[i]["Register_Counts"], address=sensor_configurations[i]["Start_Address"], unit=sensor_configurations[i]["Device_ID"])
#                         Sensor_Reading_check = str(Sensor_Reading)

#                         if Sensor_Reading_check == Modbus_Error_Message:
#                             Connection_Checking_Count = Connection_Checking_Count+1
#                             if Connection_Checking_Count == 10:
#                                 sensor_result.append(
#                                     sensor_details | Modbus_Error)
#                                 break

#                         elif Sensor_Reading_check == Modbus_Slave_Id_Error_Message:
#                             sensor_result.append(
#                                 sensor_details | Modbus_Slave_Id_Error)
#                             break

#                         elif Sensor_Reading_check == Power_Error_Message:
#                             sensor_result.append(sensor_details | Power_Error)
#                             break

#                         else:
#                             sensor_result.append(Sensor_Reading.registers)
#                             break
#                 print(sensor_result)
#                 return sensor_result
#             else:
#                 Data_Logs().Error_log(Validation_Error["MKC1"])
#                 return Validation_Error["MKC1"]
#         except FileNotFoundError:
#             Data_Logs().Error_log(Validation_Error["MKC2"])
#             return Validation_Error["MKC2"]
# {'Time': 15, 'Energymeter': [170, 1, 46], 'COD': [100, 9729, 10], 'BOD': [100, 9729, 10], 'Temperature': [100, 9729, 10], 'TSS': [100, 4608, 4], 'Ph': [110, 9729, 5], 'TDS': [120, 9729, 4], 'Conductivity': [120, 9729, 4]}



from Azure_Communication import Send_Sensor_Datas
from Azure_Communication import Receive_Azure_Data
from azure.iot.device import IoTHubDeviceClient
from General_Configurations import Sending_Iot_Connection_String, Validation_Error
from threading import Event
import threading
from Logging_Info import Data_Logs
from Reception import main


def final_data_config():
    try:
        iothub_client = IoTHubDeviceClient.create_from_connection_string(
            Sending_Iot_Connection_String)
        while True:
            Send_Sensor_Datas.Read_Sensor_Datas().send_full_sensor_readings(iothub_client)
            Receive_Azure_Data.azure_data_config(iothub_client)

            Event().wait(3)
    except ValueError:
        Data_Logs().error_log(Validation_Error["MKC15"])
        return Validation_Error["MKC15"]
    except TypeError:
        Data_Logs().error_log(Validation_Error["MKC16"])
        return Validation_Error["MKC16"]


if __name__ == '__main__':
    t1 = threading.Thread(target=final_data_config)
    t1.start()
    t2 = threading.Thread(target=main)
    t2.start()
    t2.join()