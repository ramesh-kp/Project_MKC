import json
from pymodbus.client.sync import ModbusTcpClient

from General_Configurations import Gateway_Ip_Address, Gateway_Port, Sensor_Configuration_File, Validation_Error
from General_Configurations import Modbus_Error_Message, Modbus_Error, Modbus_Slave_Id_Error_Message, Modbus_Slave_Id_Error, Power_Error_Message, Power_Error
from Logging_Info import Data_Logs


class Device_Reading():
    def gateway_connect(self):
        '''
        Description:        Establish connection of sensor with raspberry pi.
        Input Parameters:   None
        Output Type:        Object ModbusClient
        '''
        gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
        gateway_client.connect()
        return gateway_client

    def get_sensor_reading(self, sensor):
        '''
        Description:        Returns sensor readings of the sensor given in the input parameter.
        Input Parameters:   sensor configurations
        Output Type:        sensor readings
        '''
        try:
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
                        Sensor_Reading = self.gateway_connect().read_holding_registers(
                            count=sensor_configurations[i]["Register_Counts"], address=sensor_configurations[i]["Start_Address"], unit=sensor_configurations[i]["Device_ID"])
                        Sensor_Reading_check = str(Sensor_Reading)

                        if Sensor_Reading_check == Modbus_Error_Message:
                            Connection_Checking_Count = Connection_Checking_Count+1
                            if Connection_Checking_Count == 10:
                                sensor_result.append(
                                    sensor_details | Modbus_Error)
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
            else:
                Data_Logs().Error_log(Validation_Error["MKC1"])
                return Validation_Error["MKC1"]
        except FileNotFoundError:
            Data_Logs().Error_log(Validation_Error["MKC2"])
            return Validation_Error["MKC2"]
