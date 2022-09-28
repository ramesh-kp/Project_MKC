"""
This document demonstrates function in relation with Temperature Sensor
"""
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
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
    Temperature,
    ValidationError)
from logging_info import Datalogs


connection_checking_count = 0
sensor_result = {}

class TemperatureSensor(object):
    """
    This class contain functions which initilize configurations of Temperature and its array position for getting the
    Temperature data from the Temperature reading.It contain functions which reads the data from Temperature Sensor.
    """
    def __init__(self):
        config_list = []
        self.temperature_configurations = None
        self.temperature_data_position = [0, 1]
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r") as file:
            file_data = json.load(file)
            if 'Temperature_Configurations' in file_data:
                for i in range(len(file_data["Temperature_Configurations"])):
                    config_list.append(
                        list(file_data["Temperature_Configurations"][i].values()))
                self.temperature_configurations = config_list

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
                        Temperature, position): self.temperature_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(Temperature, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                    Temperature, position): self.temperature_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(Temperature, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(Temperature, position): self.temperature_configurations[position][0], SensorConfigurations[SensorGetData].format(
                    Temperature): Conversion().parse_rawdata(sensor_reading.registers, self.temperature_data_position[0], self.temperature_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("temperature_check_error_message::", ex)
            return ex

    def get_temperature_reading(self):
        try:
            temperature_data = {}
            for pos in range(len(self.temperature_configurations)):
                while True:
                    temperature_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.temperature_configurations[pos][2],
                        address=self.temperature_configurations[pos][1],
                        unit=self.temperature_configurations[pos][0]))
                    temperature_data.update(self.check_error_message(temperature_reading, pos))
                    if None not in temperature_data.values():
                        break
            return temperature_data

        except AttributeError as e:
            Datalogs().logging_error(e,"Temperature_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"Temperature_Error.log")
            print("get_temperature_reading::", ex)
            return ex

    def set_temperature_configurations(self, data):
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r+") as file:
            file_data = json.load(file)
            new_configuration = {"Device_ID": list(data.values())[0][0], "Start_Address": list(
                data.values())[0][1], "Register_Counts": list(data.values())[0][2]}
            file_data["Temperature_Configurations"].append(new_configuration)
            unsorted_configuration = [dict(t) for t in {tuple(
                d.items()) for d in file_data["Temperature_Configurations"]}]
            file_data["Temperature_Configurations"] = sorted(
                unsorted_configuration, key=lambda i: i['Device_ID'])
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def set_slave_id(self, new_slave_id):
        try:
            with open("Configurations_and_Errors/Sensor_Addresses.json", 'r') as file:
                data = json.load(file)
                sensor_address = data["Device_Address"]["Temperature_Start_Address"]
                sensor_id = data["Device_ID"]["Temperature_Default_Id"]
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

# TemperatureSensor().get_temperature_reading()