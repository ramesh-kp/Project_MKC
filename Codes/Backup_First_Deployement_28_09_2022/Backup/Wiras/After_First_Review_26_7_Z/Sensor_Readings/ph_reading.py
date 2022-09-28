"""
This document demonstrates function in relation with PH Sensor
"""
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC22,
    PH,
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


class PhSensor(object):
    """
    This class contain functions which initilize configurations of PH and its array position for getting the PH data
    from the PH reading.It contain functions which reads the data from PH Sensor.
    """

    def __init__(self):
        self.ph_configurations = [[110, 9729, 5]]
        self.ph_data_position = [2, 3]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    PH): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"Ph_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        PH): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"Ph_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    PH): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"Ph_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(PH):
                                      self.ph_configurations[0][0], SensorConfigurations[SensorGetData].format(
                    PH): Conversion().parse_rawdata(sensor_reading.registers, self.ph_data_position[0],
                                                   self.ph_data_position[1])})
                print(sensor_result)
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"Ph_Error.log")
            return ex

    def get_ph_reading(self):
        try:
            for pos in range(len(self.ph_configurations)):
                while True:
                    ph_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.ph_configurations[pos][2],
                        address=self.ph_configurations[pos][1],
                        unit=self.ph_configurations[pos][0]))
                    ph_result = self.check_error_message(ph_reading)
                    if None not in ph_result.values():
                        return ph_result
        except AttributeError as e:
            Datalogs().logging_error(e,"Ph_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"Ph_Error.log")
            return ex
