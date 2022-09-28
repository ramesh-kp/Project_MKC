"""
This document demonstrates function in relation with TDS Sensor
"""
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC22,
    TDS,
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


class TDSSensor(object):
    """
    This class contain functions which initilize configurations of TDS and its array position for getting the TDS data
    from the TDS reading.It contain functions which reads the data from TDS Sensor.
    """
    def __init__(self):
        self.tds_configurations = [[120, 9729, 4]]
        self.tds_data_position = [2, 3]

    def check_error_message(self, sensor_reading):
        try:
            global connection_checking_count
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[PowerErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    TDS): ValidationError[MKC22]})
                Datalogs().logging_error(ValidationError[MKC22],"TDS_Error.log")
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                        TDS): ValidationError[MKC17]})
                    Datalogs().logging_error(ValidationError[MKC17],"TDS_Error.log")
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({ErrorMessages[ErrorMessageSensor].format(
                    TDS): ValidationError[MKC21]})
                Datalogs().logging_error(ValidationError[MKC21],"TDS_Error.log")
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(TDS):
                                      self.tds_configurations[0][0], SensorConfigurations[SensorGetData].format(
                    TDS): Conversion().parse_rawdata(sensor_reading.registers, self.tds_data_position[0],
                                                    self.tds_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex,"TDS_Error.log")
            return ex

    def get_tds_reading(self):
        try:
            for pos in range(len(self.tds_configurations)):
                while True:
                    tds_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tds_configurations[pos][2],
                        address=self.tds_configurations[pos][1],
                        unit=self.tds_configurations[pos][0]))
                    tds_result = self.check_error_message(tds_reading)
                    if None not in tds_result.values():
                        return tds_result
        except AttributeError as e:
            Datalogs().logging_error(e,"TDS_Error.log")
        except Exception as ex:
            Datalogs().logging_error(ex,"TDS_Error.log")
            return ex
