"""
This document demonstrates function in relation with Temperature Sensor
"""
import copy
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC28,
    Configurations_File,
    Device_already_exists,
    ErrorMessageSensor,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    Sensor_Address_File,
    SensorConfigurations,
    SensorGetAddress,
    SensorGetData,
    SensorGetDefaultID,
    SensorGetDeviceID,
    SensorGetRegisterCounts,
    SensorGetStartAddress,
    SensorsError,
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
        with open(Configurations_File, "r") as file:
            file_data = json.load(file)
            if SensorConfigurations.format(Temperature) in file_data:
                for i in range(len(file_data[SensorConfigurations.format(Temperature)])):
                    config_list.append(
                        list(file_data[SensorConfigurations.format(Temperature)][i].values()))
                self.temperature_configurations = config_list

    def validate_content(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ModbusErrorMessage:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorGetDeviceID.format(
                        Temperature, position): self.temperature_configurations[position][0],
                                          ErrorMessageSensor.format(Temperature, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(
                    Temperature, position): self.temperature_configurations[position][0],
                                      ErrorMessageSensor.format(Temperature, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(Temperature, position):
                    self.temperature_configurations[position][0], SensorGetData.format(
                    Temperature, position): Conversion().parse_rawdata(sensor_reading.registers,
                                                                       self.temperature_data_position[0],
                                                                       self.temperature_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("temperature_check_error_message::", ex)
            return {ErrorMessageSensor.format(
                        Temperature, position): ValidationError[MKC28]}

    def get_temperature_reading(self):
        try:
            temperature_data = {}
            for pos in range(len(self.temperature_configurations)):
                while True:
                    temperature_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.temperature_configurations[pos][2],
                        address=self.temperature_configurations[pos][1],
                        unit=self.temperature_configurations[pos][0]))
                    temperature_data.update(
                        self.validate_content(temperature_reading, pos))
                    if None not in temperature_data.values():
                        break
            return temperature_data
        except Exception as ex:
            print("get_temperature_reading::", ex)
            return ({ErrorMessageSensor.format(
                        Temperature, pos): ValidationError[MKC28]})

    @classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]
                                      ][SensorGetStartAddress[:-3].format(Temperature)]
                sensor_id = data[SensorGetDeviceID[3:-3]
                                 ][SensorGetDefaultID[:-3].format(Temperature)]
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

    @classmethod
    def set_temperature_configurations(cls, data):
        with open(Configurations_File, "r+") as file:
            file_data = json.load(file)
            new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0], SensorGetStartAddress[3:-3]: list(
                data.values())[0][1], SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
            count = 0
            for position in range(len(file_data[SensorConfigurations.format(Temperature)])):
                if file_data[SensorConfigurations.format(Temperature)][position][SensorGetDeviceID[3:-3]] == \
                        new_configuration[SensorGetDeviceID[3:-3]]:
                    count = count+1
                    print(Device_already_exists)
                # else:
                    # file_data[SensorConfigurations.format(
                    #     Temperature)].append(
                    #     new_configuration)
                    # unsorted_configuration = [dict(t) for t in {tuple(
                    #     d.items()) for d in file_data[SensorConfigurations.format(Temperature)]}]
                    # file_data[SensorConfigurations.format(Temperature)] = sorted(
                    #     unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
            if count == 0:
                file_data[SensorConfigurations.format(
                        Temperature)].append(
                        new_configuration)
                unsorted_configuration = [dict(t) for t in {tuple(
                    d.items()) for d in file_data[SensorConfigurations.format(Temperature)]}]
                file_data[SensorConfigurations.format(Temperature)] = sorted(
                    unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            # ########self.set_slave_id(new_configuration["Device_ID"])

    def temperature_reinitiliaze(self, temperature_flag_check):
        if temperature_flag_check == True:
            self.temperature_configurations = None
        else:
            print("ReIntilization unsucessful due to writing failed.")

    def remove_temperature_configurations(self, device_id, temperature_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                temperature_data = file_data_change[SensorConfigurations.format(
                    Temperature)]
                for index in range(len(temperature_data)):
                    if temperature_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.temperature_reinitiliaze(temperature_flag_check)
                        del temperature_data[index]
                        break
                if check_con == 0:
                    print("Temperature DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(
                    Temperature)] = temperature_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(Temperature))
            print("exception in remove_temperature_configurations", ex)
            return ex
