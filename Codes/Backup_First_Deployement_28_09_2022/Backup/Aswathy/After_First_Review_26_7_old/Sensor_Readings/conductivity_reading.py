"""
This document demonstrates function in relation with Conductivity Sensor
"""
import copy
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import (
    MKC17,
    MKC21,
    MKC28,
    Conductivity,
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
    ValidationError)
from logging_info import Datalogs


connection_checking_count = 0
sensor_result = {}


class ConductivitySensor(object):
    """
    This class contain functions which initilize configurations of Conductivity and its array position for getting the
    Conductivity data from the Conductivity reading.It contain functions which reads the data from Conductivity Sensor.
    """

    def __init__(self):
        config_list = []
        self.conductivity_configurations = None
        self.conductivity_data_position = [0, 1]
        with open(Configurations_File, "r") as file:
            file_data = json.load(file)
            if SensorConfigurations.format(Conductivity) in file_data:
                for i in range(len(file_data[SensorConfigurations.format(Conductivity)])):
                    config_list.append(
                        list(file_data[SensorConfigurations.format(Conductivity)][i].values()))
                self.conductivity_configurations = config_list

    def validate_content(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ModbusErrorMessage:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorGetDeviceID.format(Conductivity, position):
                                          self.conductivity_configurations[position][0],
                                          ErrorMessageSensor.format(Conductivity, position):
                                          ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(Conductivity, position):
                                      self.conductivity_configurations[position][0],
                                      ErrorMessageSensor.format(Conductivity, position):
                                      ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(Conductivity, position):
                                      self.conductivity_configurations[position][0],
                                      SensorGetData.format(Conductivity, position):
                                      Conversion().parse_rawdata(sensor_reading.registers,
                                                                 self.conductivity_data_position[0],
                                                                 self.conductivity_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("conductivity_check_error_message::", ex)
            return {ErrorMessageSensor.format(
                        Conductivity, position):ValidationError[MKC28]}


    def get_conductivity_reading(self):
        try:
            conductivity_data = {}
            for pos in range(len(self.conductivity_configurations)):
                while True:
                    conductivity_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.conductivity_configurations[pos][2],
                        address=self.conductivity_configurations[pos][1],
                        unit=self.conductivity_configurations[pos][0]))
                    conductivity_data.update(
                        self.validate_content(conductivity_reading, pos))
                    if None not in conductivity_data.values():
                        break
            return conductivity_data
        except Exception as ex:
            print("get_conductivity_reading::", ex)
            return {ErrorMessageSensor.format(
                        Conductivity, pos): ValidationError[MKC28]}

    @classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]
                                      ][SensorGetStartAddress[:-3].format(Conductivity)]
                sensor_id = data[SensorGetDeviceID[3:-3]
                                 ][SensorGetDefaultID[:-3].format(Conductivity)]
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
    def set_conductivity_configurations(cls, data):
        with open(Configurations_File, "r+") as file:
            file_data = json.load(file)
            new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0],
                                 SensorGetStartAddress[3:-3]: list(data.values())[0][1],
                                 SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
            count = 0
            for position in range(len(file_data[SensorConfigurations.format(Conductivity)])):
                if file_data[SensorConfigurations.format(Conductivity)][position][SensorGetDeviceID[3:-3]] == \
                        new_configuration[SensorGetDeviceID[3:-3]]:
                    count = count+1
                    print(Device_already_exists)
                # else:
                    # file_data[SensorConfigurations.format(
                    #     Conductivity)].append(new_configuration)
                    # unsorted_configuration = [dict(t) for t in {tuple(
                    #     d.items()) for d in file_data[SensorConfigurations.format(Conductivity)]}]
                    # file_data[SensorConfigurations.format(Conductivity)] = sorted(
                    #     unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
            if count == 0:
                file_data[SensorConfigurations.format(
                        Conductivity)].append(new_configuration)
                unsorted_configuration = [dict(t) for t in {tuple(
                    d.items()) for d in file_data[SensorConfigurations.format(Conductivity)]}]
                file_data[SensorConfigurations.format(Conductivity)] = sorted(
                    unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            # ########self.set_slave_id(new_configuration["Device_ID"])

    def conductivity_reinitiliaze(self, conductivity_flag_check):
        if conductivity_flag_check == True:
            self.conductivity_configurations = None
        else:
            print("ReIntilization unsucessful due to writing failed.")

    def remove_conductivity_configurations(self, device_id, conductivity_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                conductivity_data = file_data_change[SensorConfigurations.format(
                    Conductivity)]
                for index in range(len(conductivity_data)):
                    if conductivity_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.conductivity_reinitiliaze(conductivity_flag_check)
                        del conductivity_data[index]
                        break
                if check_con == 0:
                    print("Conductivity DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(
                    Conductivity)] = conductivity_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(Conductivity))
            print("exception in remove_conductivity_configurations", ex)
            return ex
