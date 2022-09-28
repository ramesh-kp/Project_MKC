"""
This document demonstrates function in relation with COD Sensor
"""
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion

from general_configurations import (
    COD,
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


class CODSensor(object):
    """
    This class contain functions which initilize configurations of COD and its array position for getting the COD data
    from the COD reading.It contain functions which reads the data from COD Sensor.
    """

    def __init__(self):
        self.cod_configurations = [[100, 9729, 10]]
        self.cod_data_position = [2, 3]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    COD): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"COD_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        COD): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"COD_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    COD): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"COD_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(COD):
                                      self.cod_configurations[0][0], SensorConfigurations[SensorGetData].format(
                    COD): Conversion().parse_rawdata(sensor_reading.registers, self.cod_data_position[0],
                                                    self.cod_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"COD_Error.log")
            return ex

    def get_cod_reading(self):
        try:
            for pos in range(len(self.cod_configurations)):
                while True:
                    cod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.cod_configurations[pos][2],
                        address=self.cod_configurations[pos][1],
                        unit=self.cod_configurations[pos][0]))
                    cod_result = self.check_error_message(cod_reading)
                    if None not in cod_result.values():
                        return cod_result
        except AttributeError as e:
            Datalogs().logging_error(e,"COD_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"COD_Error.log")
            return ex
