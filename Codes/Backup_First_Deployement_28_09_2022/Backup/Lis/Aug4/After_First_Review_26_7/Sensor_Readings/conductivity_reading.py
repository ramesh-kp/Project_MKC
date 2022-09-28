"""
This document demonstrates function in relation with Conductivity Sensor
"""
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import (
    MKC17,
    MKC21,
    MKC22,
    Conductivity,
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


class ConductivitySensor(object):
    """
    This class contain functions which initilize configurations of Conductivity and its array position for getting the
    Conductivity data from the Conductivity reading.It contain functions which reads the data from Conductivity Sensor.
    """
    def __init__(self):
        self.conductivity_configurations = [[120, 9729, 4]]
        self.conductivity_data_position = [0, 1]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    Conductivity): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"Conductivity_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        Conductivity): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"Conductivity_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    Conductivity): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"Conductivity_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(Conductivity):
                                      self.conductivity_configurations[0][0],
                                      SensorConfigurations[SensorGetData].format(Conductivity): round(Conversion(
                                        ).parse_rawdata(sensor_reading.registers, self.conductivity_data_position[0],
                                                             self.conductivity_data_position[1])/10, 2)})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"Conductivity_Error.log")
            return ex

    def get_conductivity_reading(self):
        try:
            for pos in range(len(self.conductivity_configurations)):
                while True:
                    conductivity_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.conductivity_configurations[pos][2],
                        address=self.conductivity_configurations[pos][1],
                        unit=self.conductivity_configurations[pos][0]))
                    conductivity_result = self.check_error_message(
                        conductivity_reading)
                    if None not in conductivity_result.values():
                        return conductivity_result
        except AttributeError as e:
            Datalogs().logging_error(e,"Conductivity_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"Conductivity_Error.log")
            return ex
