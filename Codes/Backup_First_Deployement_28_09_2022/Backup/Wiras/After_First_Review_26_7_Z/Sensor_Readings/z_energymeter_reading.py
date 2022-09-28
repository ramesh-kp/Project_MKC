"""
This document demonstrates function in connection with Energymeter sensor
"""
import json
from Utilities.util_device_communication import DeviceCommunication
from general_configurations import (
    MKC17,
    MKC21,
    MKC22,
    Energymeter,
    EnergymeterCkah,
    EnergymeterCkwh,
    EnergymeterConfiguration,
    EnergymeterDeviceID,
    EnergymeterFrequency,
    EnergymeterPowerFactorLine1,
    EnergymeterPowerFactorLine2,
    EnergymeterPowerFactorLine3,
    EnergymeterTotalPowerFactor,
    EnergymeterVoltage,
    ErrorMessageSensor,
    ErrorMessages,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    PowerErrorMessage,
    SensorConfigurations,
    SensorGetDeviceID,
    ValidationError
)
from logging_info import Datalogs

connection_checking_count = 0


class EnergymeterSensor(object):
    """
    This class consist of functions in relation with the Energymeter Sensor.
    """

    def __init__(self):
        config_list = []
        self.energymeter_configurations = None
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r") as file:
            file_data = json.load(file)
            if 'Energymeter_Configurations' in file_data:
                for i in range(len(file_data["Energymeter_Configurations"])):
                    config_list.append(
                        list(file_data["Energymeter_Configurations"][i].values()))
                self.energymeter_configurations = config_list

    @classmethod
    def parse_rawdata_energymeter(cls, energymeter_reading_raw, position):
        energymeter_final_data = {}
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
                EnergymeterConfiguration[EnergymeterDeviceID]: slave_id,
                EnergymeterConfiguration[EnergymeterCkwh]: ckwh,
                EnergymeterConfiguration[EnergymeterCkah]: ckah,
                EnergymeterConfiguration[EnergymeterVoltage]: voltage,
                EnergymeterConfiguration[EnergymeterPowerFactorLine1]: power_factor_line_1,
                EnergymeterConfiguration[EnergymeterPowerFactorLine2]: power_factor_line_2,
                EnergymeterConfiguration[EnergymeterPowerFactorLine3]: power_factor_line_3,
                EnergymeterConfiguration[EnergymeterTotalPowerFactor]: total_power_factor,
                EnergymeterConfiguration[EnergymeterFrequency]: frequency,
            }
            energy_meter_data["Energymeter_Device_ID_{}".format(0)] = slave_id
            print()
            print(energy_meter_data)
            print()
            return energymeter_final_data
        except Exception as ex:
            return ex

    def check_error_message(self, sensor_reading, position):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                        Energymeter, position): self.energymeter_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(
                        Energymeter, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                    Energymeter, position): self.energymeter_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(
                    Energymeter, position): ValidationError[MKC21]})
            else:
                sensor_result.update(self.parse_rawdata_energymeter(
                    sensor_reading.registers, position))
            return sensor_result
        except Exception as ex:
            print("energymeter_check_error_message::", ex)
            return ex

    def get_energymeter_reading(self):
        try:
            energymeter_data = {}
            for pos in range(len(self.energymeter_configurations)):
                while True:
                    energymeter_reading = (DeviceCommunication().gateway_connect().read_holding_registers(
                        count=self.energymeter_configurations[pos][2],
                        address=self.energymeter_configurations[pos][1],
                        unit=self.energymeter_configurations[pos][0]))
                    energymeter_data.update(self.check_error_message(
                        energymeter_reading, pos))
                    if None not in energymeter_data.values():
                        break
            return energymeter_data
        except Exception as ex:
            print("get_energymeter_reading_exception::", ex)
            return ex

    def set_energymeter_configurations(self, data):
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r+") as file:
            file_data = json.load(file)
            new_configuration = {"Device_ID": list(data.values())[0][0], "Start_Address": list(
                data.values())[0][1], "Register_Counts": list(data.values())[0][2]}
            file_data["Energymeter_Configurations"].append(new_configuration)
            unsorted_configuration = [dict(t) for t in {tuple(
                d.items()) for d in file_data["Energymeter_Configurations"]}]
            file_data["Energymeter_Configurations"] = sorted(
                unsorted_configuration, key=lambda i: i['Device_ID'])
            file.seek(0)
            json.dump(file_data, file, indent=4)
