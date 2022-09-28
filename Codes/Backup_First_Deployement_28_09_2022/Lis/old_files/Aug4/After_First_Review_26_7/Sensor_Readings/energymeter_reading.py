"""
This document demonstrates function in connection with Energymeter sensor
"""
from Utilities.util_device_communication import DeviceCommunication
from general_configurations import (
    MKC17,
    MKC21,
    MKC22,
    MKC28,
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
    ModbusConnectionError,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    PowerErrorMessage,
    ValidationError
)
from logging_info import Datalogs

connection_checking_count = 0
energymeter_final_data = {}

class EnergymeterSensor(object):
    """
    This class consist of functions in relation with the Energymeter Sensor.
    """

    def __init__(self):
        self.energymeter_configurations = [[170, 1, 46]]

    @classmethod
    def parse_rawdata_energymeter(cls, energymeter_reading_raw, pos):
        global energymeter_final_data
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
            energymeter_final_data.update({slave_id : energy_meter_data})
            print("####",energymeter_final_data)
            # energy_meter_data["EnergymeterDeviceID_{}".format(pos)] = slave_id
            # energy_meter_data.pop(list(energy_meter_data.keys())[0])
            # energy_meter_data = dict([energy_meter_data.popitem()]) | energy_meter_data
            return energymeter_final_data
        except Exception as ex:
            Datalogs().logging_error(ex,"Energymeter_Error.log")
            return ex

    def check_error_message(self, sensor_reading, position):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    Energymeter): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"Energymeter_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        Energymeter): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"Energymeter_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    Energymeter): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"Energymeter_Error.log")
            # elif sensor_reading_check == ErrorMessages[ModbusConnectionError]:
            #     sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
            #         Energymeter): ValidationError[MKC28]})
            else:
                sensor_result.update(
                    self.parse_rawdata_energymeter(sensor_reading.registers, position))
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"Energymeter_Error.log")
            return ex

    def get_energymeter_reading(self):
        try:
            energymeter_result = {}
            for pos in range(len(self.energymeter_configurations)):
                while True:
                    energymeter_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.energymeter_configurations[pos][2],
                        address=self.energymeter_configurations[pos][1],
                        unit=self.energymeter_configurations[pos][0]))
                    energymeter_result = self.check_error_message(
                        energymeter_reading, pos)
                    if None not in energymeter_result.values():
                        return energymeter_result
        except AttributeError as e:
            Datalogs().logging_error(e,"Energymeter_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"Energymeter_Error.log")
            return ex
