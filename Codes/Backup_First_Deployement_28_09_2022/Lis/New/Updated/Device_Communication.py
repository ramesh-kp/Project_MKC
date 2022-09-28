import json
from pymodbus.client.sync import ModbusTcpClient

from General_Configurations import Gateway_Ip_Address, Gateway_Port, Sensor_Configuration_File
from General_Configurations import Modbus_Error_Message, Modbus_Error, Modbus_Slave_Id_Error_Message, Modbus_Slave_Id_Error, Power_Error_Message, Power_Error


class Device_Reading():
    def Gateway_Connect(self):
        gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
        gateway_client.connect()
        return gateway_client

    def Get_Sensor_Reading(self, sensor):
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
                    Sensor_Reading = self.Gateway_Connect().read_holding_registers(
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
# a = Device_Reading().Get_Sensor_Reading("BOD")
# print(a)