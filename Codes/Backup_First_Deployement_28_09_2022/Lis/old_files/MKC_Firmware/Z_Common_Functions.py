import json
from pymodbus.client.sync import ModbusTcpClient
from General_Configurations import *

result = []


def Gateway_Connect():
    gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
    gateway_client.connect()
    return gateway_client


def Reading_Sensors(sensor):
    Connection_Checking_Count = 0
    sensor = "{}_Configurations".format(sensor)
    with open("Sensor_Configuration.json", 'r') as file:
        data = json.load(file)
    if sensor in data:
        sensor_configurations = data[sensor]
        for i in range(len(sensor_configurations)):
            sensor_details = {"Sensor": sensor, "Number": i+1}
            while True:
                Sensor_Reading = Gateway_Connect().read_holding_registers(
                    count=sensor_configurations[i]["Register_Counts"], address=sensor_configurations[i]["Start_Address"], unit=sensor_configurations[i]["Device_ID"])
                Sensor_Reading_check = str(Sensor_Reading)

                if Sensor_Reading_check == Modbus_Error_Message:
                    Connection_Checking_Count = Connection_Checking_Count+1
                    if Connection_Checking_Count == 10:
                        result.append(sensor_details | Modbus_Error)
                        break

                elif Sensor_Reading_check == Modbus_Slave_Id_Error_Message:
                    result.append(sensor_details | Modbus_Slave_Id_Error)
                    break

                elif Sensor_Reading_check == Power_Error_Message:
                    result.append(sensor_details | Power_Error)
                    break

                else:
                    result.append(Sensor_Reading.registers)
                    break
        return result


if __name__ == '__main__':
    a = Reading_Sensors("Energymeter")
    print(a)
