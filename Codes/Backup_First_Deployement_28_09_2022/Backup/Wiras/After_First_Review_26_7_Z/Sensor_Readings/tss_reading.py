"""
This document demonstrates function in relation with TSS Sensor
"""
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC22,
    TSS,
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


class TSSSensor(object):
    """
    This class contain functions which initilize configurations of TSS and its array position for getting the TSS data
    from the TSS reading.It contain functions which reads the data from TSS Sensor.
    """

    def __init__(self):
        self.tss_configurations = [[100, 4608, 4]]
        self.tss_data_position = [0, 1]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    TSS): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"TSS_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        TSS): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"TSS_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    TSS): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"TSS_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(TSS):
                                      self.tss_configurations[0][0], SensorConfigurations[SensorGetData].format(
                    TSS): Conversion().parse_rawdata(sensor_reading.registers, self.tss_data_position[0],
                                                    self.tss_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"TSS_Error.log")
            return ex

    def get_tss_reading(self):
        try:
            for pos in range(len(self.tss_configurations)):
                while True:
                    tss_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tss_configurations[pos][2],
                        address=self.tss_configurations[pos][1],
                        unit=self.tss_configurations[pos][0]))
                    tss_result = self.check_error_message(tss_reading)
                    if None not in tss_result.values():
                        return tss_result
        except AttributeError as e:
            Datalogs().logging_error(e,"TSS_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"TSS_Error.log")
            return ex
