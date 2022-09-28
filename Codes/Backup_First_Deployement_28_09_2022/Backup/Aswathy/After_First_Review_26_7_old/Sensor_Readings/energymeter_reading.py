"""
This document demonstrates function in connection with Energymeter sensor
"""
import json
import copy
from Utilities.util_device_communication import DeviceCommunication
from general_configurations import (
    MKC17,
    MKC21,
    MKC28,
    Configurations_File,
    Energymeter,
    EnergymeterCkah,
    EnergymeterCkwh,
    EnergymeterDeviceID,
    EnergymeterFrequency,
    EnergymeterPowerFactorLine1,
    EnergymeterPowerFactorLine2,
    EnergymeterPowerFactorLine3,
    EnergymeterTotalPowerFactor,
    EnergymeterVoltage,
    ErrorMessageSensor,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    SensorConfigurations,
    SensorGetDeviceID,
    SensorGetRegisterCounts,
    SensorGetStartAddress,
    SensorsError,
    ValidationError
)
from logging_info import Datalogs

connection_checking_count = 0
sensor_result = {}
energymeter_data = {}


class EnergymeterSensor(object):
    """
    This class consist of functions in relation with the Energymeter Sensor.
    """

    def __init__(self):
        config_list = []
        self.energymeter_configurations = None
        with open(Configurations_File, "r") as file:
            file_data = json.load(file)
            if SensorConfigurations.format(Energymeter) in file_data:
                for i in range(len(file_data[SensorConfigurations.format(Energymeter)])):
                    config_list.append(
                        list(file_data[SensorConfigurations.format(Energymeter)][i].values()))
                self.energymeter_configurations = config_list

    @classmethod
    def parse_rawdata_energymeter(cls, energymeter_reading_raw, position):
        try:
            slave_id = energymeter_reading_raw[1]
            ckwh = energymeter_reading_raw[5] / 1000
            ckah = energymeter_reading_raw[7] / 1000
            voltage = energymeter_reading_raw[9] / 10
            power_factor_line_1 = energymeter_reading_raw[33] / 100
            power_factor_line_2 = energymeter_reading_raw[35] / 100
            power_factor_line_3 = energymeter_reading_raw[37] / 100
            total_power_factor = energymeter_reading_raw[43] / 100
            frequency = energymeter_reading_raw[45] / 10
            energy_meter_data = {
                EnergymeterDeviceID.format(position): slave_id,
                EnergymeterCkwh.format(position): ckwh,
                EnergymeterCkah.format(position): ckah,
                EnergymeterVoltage.format(position): voltage,
                EnergymeterPowerFactorLine1.format(position): power_factor_line_1,
                EnergymeterPowerFactorLine2.format(position): power_factor_line_2,
                EnergymeterPowerFactorLine3.format(position): power_factor_line_3,
                EnergymeterTotalPowerFactor.format(position): total_power_factor,
                EnergymeterFrequency.format(position): frequency,
            }
            return energy_meter_data
        except Exception as ex:
            return ex

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
                        Energymeter, position): self.energymeter_configurations[position][0], ErrorMessageSensor.format(
                        Energymeter, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(
                    Energymeter, position): self.energymeter_configurations[position][0], ErrorMessageSensor.format(
                    Energymeter, position): ValidationError[MKC21]})
            else:
                sensor_result.update(self.parse_rawdata_energymeter(
                    sensor_reading.registers, position))
            return sensor_result
        except Exception as ex:
            return {ErrorMessageSensor.format(
                        Energymeter, position):ValidationError[MKC28]}

    def get_energymeter_reading(self):
        try:
            global energymeter_data
            for pos in range(len(self.energymeter_configurations)):
                while True:
                    energymeter_reading = (DeviceCommunication().gateway_connect().read_holding_registers(
                        count=self.energymeter_configurations[pos][2],
                        address=self.energymeter_configurations[pos][1],
                        unit=self.energymeter_configurations[pos][0]))
                    energymeter_data.update(self.validate_content(
                        energymeter_reading, pos))
                    if None not in energymeter_data.values():
                        break
            return energymeter_data
        except AttributeError as e:
            return e
        except Exception as ex:
            return({ErrorMessageSensor.format(
                        Energymeter, pos): ValidationError[MKC28]})

    @classmethod
    def set_energymeter_configurations(cls, data):
        try:
            with open(Configurations_File, "r+") as file:
                file_data = json.load(file)
                new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0], SensorGetStartAddress[3:-3]: list(
                    data.values())[0][1], SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
                file_data[SensorConfigurations.format(Energymeter)].append(new_configuration)
                unsorted_configuration = [dict(t) for t in {tuple(
                    d.items()) for d in file_data[SensorConfigurations.format(Energymeter)]}]
                file_data[SensorConfigurations.format(Energymeter)] = sorted(
                    unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            return ex

    def energymeter_reinitiliaze(self, energymeter_flag_check):
        if energymeter_flag_check == True:
            self.energymeter_configurations = None
        else:
            print("ReIntilization unsucessful due to writing failed.")

    def remove_energymeter_configurations(self, device_id, energymeter_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                energymeter_data = file_data_change[SensorConfigurations.format(Energymeter)]
                for index in range(len(energymeter_data)):
                    if energymeter_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.energymeter_reinitiliaze(energymeter_flag_check)
                        del energymeter_data[index]
                        break
                if check_con ==0:
                    print("Energymeter DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(Energymeter)] = energymeter_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(Energymeter))
            print("exception in remove_energymeter_configurations", ex)
            return ex
