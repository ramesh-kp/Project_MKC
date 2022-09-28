"""
This document demonstrates function in relation with Temperature Sensor
"""
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


class TemperatureSensor(object):
    """
    This class contain functions which initilize configurations of Temperature and its array position for getting the
    Temperature data from the Temperature reading.It contain functions which reads the data from Temperature Sensor.
    """
    def __init__(self):
        self.temperature_configurations = [[100, 9729, 10]]
        self.temperature_data_position = [0, 1]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    Temperature): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"Temperature_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        Temperature): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"Temperature_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    Temperature): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"Temperature_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(Temperature):
                                      self.temperature_configurations[0][0], SensorConfigurations[SensorGetData].format(
                    Temperature): Conversion().parse_rawdata(sensor_reading.registers, self.temperature_data_position[0],
                                                            self.temperature_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"Temperature_Error.log")
            return ex

    def get_temperature_reading(self):
        try:
            for pos in range(len(self.temperature_configurations)):
                while True:
                    temperature_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.temperature_configurations[pos][2],
                        address=self.temperature_configurations[pos][1],
                        unit=self.temperature_configurations[pos][0]))
                    temperature_result = self.check_error_message(
                        temperature_reading)
                    if None not in temperature_result.values():
                        return temperature_result
        except AttributeError as e:
            Datalogs().logging_error(e,"Temperature_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"Temperature_Error.log")
            return ex
