"""
This document demonstrates function in relation with BOD Sensor
"""
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    BOD,
    MKC17,
    MKC21,
    MKC22,
    ErrorMessageSensor,
    ErrorMessages,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    PowerErrorMessage,
    SensorConfigurations,
    SensorGetData,
    SensorGetDeviceID,
    ValidationError)
from logging_info import Datalogs


connection_checking_count = 0
sensor_result = {}


class BODSensor(object):
    """
    This class contain functions which initilize configurations of BOD and its array position for getting the BOD data
    from the BOD reading.It contain functions which reads the data from BOD Sensor.
    """

    def __init__(self):
        config_list = []
        self.bod_configurations = None
        self.bod_data_position = [2, 3]
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r") as file:
            file_data = json.load(file)
            if 'BOD_Configurations' in file_data:
                for i in range(len(file_data["BOD_Configurations"])):
                    config_list.append(
                        list(file_data["BOD_Configurations"][i].values()))
                self.bod_configurations = config_list

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
                        BOD, position): self.bod_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(BOD, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                    BOD, position): self.bod_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(BOD, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(BOD, position): self.bod_configurations[position][0], SensorConfigurations[SensorGetData].format(
                    BOD): Conversion().parse_rawdata(sensor_reading.registers, self.bod_data_position[0], self.bod_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("bod_check_error_message::", ex)
            return ex

    def get_bod_reading(self):
        try:
            bod_data = {}
            for pos in range(len(self.bod_configurations)):
                while True:
                    bod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.bod_configurations[pos][2],
                        address=self.bod_configurations[pos][1],
                        unit=self.bod_configurations[pos][0]))
                    bod_data.update(self.check_error_message(bod_reading, pos))
                    if None not in bod_data.values():
                        break
            return bod_data
        except Exception as ex:
            print("get_cod_reading::", ex)
            return ex

    def set_bod_configurations(self, data):
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r+") as file:
            file_data = json.load(file)
            new_configuration = {"Device_ID": list(data.values())[0][0], "Start_Address": list(
                data.values())[0][1], "Register_Counts": list(data.values())[0][2]}
            file_data["BOD_Configurations"].append(new_configuration)
            unsorted_configuration = [dict(t) for t in {tuple(
                d.items()) for d in file_data["BOD_Configurations"]}]
            file_data["BOD_Configurations"] = sorted(
                unsorted_configuration, key=lambda i: i['Device_ID'])
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def set_slave_id(self, new_slave_id):
        try:
            with open("Configurations_and_Errors/Sensor_Addresses.json", 'r') as file:
                data = json.load(file)
                sensor_address = data["Device_Address"]["BOD_Start_Address"]
                sensor_id = data["Device_ID"]["BOD_Default_Id"]
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
