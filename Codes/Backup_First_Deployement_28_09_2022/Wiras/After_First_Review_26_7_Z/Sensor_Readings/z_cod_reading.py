"""
This document demonstrates function in relation with COD Sensor
"""
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion

from general_configurations import (
    COD,
    MKC17,
    MKC21,
    ErrorMessageSensor,
    ErrorMessages,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    SensorConfigurations,
    SensorGetData,
    SensorGetDeviceID,
    ValidationError)

connection_checking_count = 0
sensor_result = {}


class CODSensor(object):
    """
    This class contain functions which initilize configurations of COD and its array position for getting the COD data
    from the COD reading.It contain functions which reads the data from COD Sensor.
    """

    def __init__(self):
        config_list = []
        self.cod_configurations = None
        self.cod_data_position = [2, 3]
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r") as file:
            file_data = json.load(file)
            if 'COD_Configurations' in file_data:
                for i in range(len(file_data["COD_Configurations"])):
                    config_list.append(
                        list(file_data["COD_Configurations"][i].values()))
                self.cod_configurations = config_list

    def check_error_message(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                        COD, position): self.cod_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(COD, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                    COD, position): self.cod_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(COD, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(COD, position): self.cod_configurations[position][0], SensorConfigurations[SensorGetData].format(
                    COD): Conversion().parse_rawdata(sensor_reading.registers, self.cod_data_position[0], self.cod_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("cod_check_error_message::", ex)
            return ex

    def get_cod_reading(self):
        try:
            cod_data = {}
            for pos in range(len(self.cod_configurations)):
                while True:
                    cod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.cod_configurations[pos][2],
                        address=self.cod_configurations[pos][1],
                        unit=self.cod_configurations[pos][0]))
                    cod_data.update(self.check_error_message(cod_reading, pos))
                    if None not in cod_data.values():
                        break
            return cod_data
        except Exception as ex:
            print("get_cod_reading::", ex)
            return ex

    def set_cod_configurations(self, data):
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r+") as file:
            file_data = json.load(file)
            new_configuration = {"Device_ID": list(data.values())[0][0], "Start_Address": list(
                data.values())[0][1], "Register_Counts": list(data.values())[0][2]}
            file_data["COD_Configurations"].append(new_configuration)
            unsorted_configuration = [dict(t) for t in {tuple(
                d.items()) for d in file_data["COD_Configurations"]}]
            file_data["COD_Configurations"] = sorted(
                unsorted_configuration, key=lambda i: i['Device_ID'])
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def set_slave_id(self, new_slave_id):
        try:
            with open("Configurations_and_Errors/Sensor_Addresses.json", 'r') as file:
                data = json.load(file)
                sensor_address = data["Device_Address"]["COD_Start_Address"]
                sensor_id = data["Device_ID"]["COD_Default_Id"]
                res = DeviceCommunication().gateway_connect().write_registers(
                    address=sensor_address,
                    values=Conversion().little_to_big_endian(new_slave_id),
                    unit=int(sensor_id))
                # address - Starting Address
                # values - Values to write
                # unit - Current Slave Id
                print(res)
        except Exception as e:
            print(e)
