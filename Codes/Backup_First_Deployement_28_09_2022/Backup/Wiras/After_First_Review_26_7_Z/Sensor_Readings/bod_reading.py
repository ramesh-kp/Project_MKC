"""
This document demonstrates function in relation with BOD Sensor
"""
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


class BODSensor(object):
    """
    This class contain functions which initilize configurations of BOD and its array position for getting the BOD data
    from the BOD reading.It contain functions which reads the data from BOD Sensor.
    """

    def __init__(self):
        self.bod_configurations = [[100, 9729, 10]]
        self.bod_data_position = [4, 5]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    BOD): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"BOD_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        BOD): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"BOD_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    BOD): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"BOD_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(BOD):
                                      self.bod_configurations[0][0], SensorConfigurations[SensorGetData].format(
                    BOD): Conversion().parse_rawdata(sensor_reading.registers, self.bod_data_position[0],
                                                    self.bod_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"BOD_Error.log")
            return ex

    def get_bod_reading(self):
        try:
            for pos in range(len(self.bod_configurations)):
                while True:
                    bod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.bod_configurations[pos][2],
                        address=self.bod_configurations[pos][1],
                        unit=self.bod_configurations[pos][0]))
                    bod_result = self.check_error_message(bod_reading)
                    if None not in bod_result.values():
                        return bod_result
        except AttributeError as e:
            Datalogs().logging_error(e,"BOD_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"BOD_Error.log")
            return ex
