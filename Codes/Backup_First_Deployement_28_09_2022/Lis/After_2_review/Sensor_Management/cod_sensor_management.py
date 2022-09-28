"""
This document demonstrates function in relation with COD Sensor
"""
import copy
import json
from unittest import result
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion

from general_configurations import (
    COD,
    MKC17,
    MKC21,
    MKC28,
    BOD_Sensor_not_found,
    Configurations_File,
    Device_already_exists,
    ErrorMessageSensor,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    Sensor_Address_File,
    SensorConfigurations,
    SensorGetAddress,
    SensorGetData,
    SensorGetDefaultID,
    SensorGetDeviceID,
    SensorGetRegisterCounts,
    SensorGetStartAddress,
    SensorsError,
    ValidationError)
from logging_info import Datalogs

connection_checking_count = 0
sensor_result = {}


class CODSensor(object):
    """
    This class contain functions which initilize configurations of COD and its array position for getting the COD data
    from the COD reading.It contain functions which reads the data from COD Sensor.
    """

    def __init__(self,deviceid):
        try:
            self.deviceid = deviceid
            config_list = []
            self.cod_start_flag = False
            self.cod_configurations = None
            self.cod_data_position = [2, 3]
            with open(CONFIGURATIONS_FILE, "r") as file:
                file_data = json.load(file)
                if SensorConfigurations.format(COD) in file_data:
                    for i in range(len(file_data[SensorConfigurations.format(COD)])):
                        config_list.append(
                            list(file_data[SensorConfigurations.format(COD)][i].values()))
                    self.cod_configurations = config_list
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(COD))

    def validate_content(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ModbusErroMODBUSERRORMESSAGErMessage:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorGetDeviceID.format(COD, position): self.cod_configurations[position][0],
                                          ErrorMessageSensor.format(COD, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(COD, position): self.cod_configurations[position][0],
                                      ErrorMessageSensor.format(COD, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(COD, position): self.cod_configurations[position][0],
                                      SensorGetData.format(COD, position): Conversion().parse_rawdata(
                    sensor_reading.registers, self.cod_data_position[0], self.cod_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(COD))
            print("cod_check_error_message::", ex)
            return {ErrorMessageSensor.format(
                        COD, position):ValidationError[MKC28]}


    def get_cod_reading(self, cod_start_flag):
        try:
            cod_data = {}
            for pos in range(len(self.cod_configurations)):
                while cod_start_flag and self.deviceid == self.cod_configurations:
                    cod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.cod_configurations[pos][2],
                        address=self.cod_configurations[pos][1],
                        unit=self.cod_configurations[pos][0]))
                    cod_data.update(self.validate_content(cod_reading, pos))
                    if None not in cod_data.values():
                        break
            Datalogs().logging_error("Received readings from Sensor", SensorsError.format(COD))
            return cod_data
        except Exception as ex:
            print("get_cod_reading::", ex)
            Datalogs().logging_error(ex, SensorsError.format(COD))
            return {ErrorMessageSensor.format(
                        COD, pos): ValidationError[MKC28]}

    def enable_reading(self):
        try:
            self.cod_start_flag = False
            result = self.get_cod_reading(self.cod_start_flag)
            return result
        except Exception as ex:
            Datalogs().logging_error(ex,SensorsError.format(COD))

    def diasble_reading(self):
        try:
            self.cod_start_flag = False
            self.get_cod_reading(self.cod_start_flag)
            Datalogs().logging_error("Reading from sensor disabled", SensorsError.format(COD))
        except Exception as ex:
            Datalogs().logging_error(ex,SensorsError.format(COD))
    @ classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]
                                      ][SensorGetStartAddress[:-3].format(COD)]
                sensor_id = data[SensorGetDeviceID[3:-3]
                                 ][SensorGetDefaultID[:-3].format(COD)]
                res = DeviceCommunication().gateway_connect().write_registers(
                    address=sensor_address,
                    values=Conversion().little_to_big_endian(new_slave_id),
                    unit=int(sensor_id))
                # address - Starting Address
                # values - Values to write
                # unit - Current Slave Id
                print(res)
        except Exception as e:
            print("exception in add_device_cod", e)
            Datalogs().logging_error(e, SensorsError.format(COD))
            return e

    @ classmethod
    def set_cod_configurations(cls, data):
        try:
            with open(CONFIGURATIONS_FILE, "r+") as file:
                file_data = json.load(file)
                new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0],
                                     SensorGetStartAddress[3:-3]: list(data.values())[0][1],
                                     SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
                count = 0
                for position in range(len(file_data[SensorConfigurations.format(COD)])):
                    if file_data[SensorConfigurations.format(COD)][position][SensorGetDeviceID[3:-3]] == \
                        new_configuration[SensorGetDeviceID[3:-3]]:
                        count = count+1
                        print(Device_already_exists)
                if count == 0:
                    file_data[SensorConfigurations.format(
                            COD)].append(new_configuration)
                    unsorted_configuration = [dict(t) for t in {tuple(
                            d.items()) for d in file_data[SensorConfigurations.format(COD)]}]
                    file_data[SensorConfigurations.format(COD)] = sorted(
                            unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
                    file.truncate(0)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                    Datalogs().logging_error("Configurations added successfully", SensorsError.format(COD))
                # ########self.set_slave_id(new_configuration["Device_ID"])
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(COD))
            print("Exception in set_cod_configurations", ex)
            return ex

    def cod_reinitiliaze(self):
        try:
            self.diasble_reading()
            self.cod_configurations = None
        except Exception as ex:
            Datalogs().logging_error(ex,SensorsError.format(COD))

    def remove_cod_configurations(self):
        try:
            check_con = 0
            with open(CONFIGURATIONS_FILE, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                cod_data = file_data_change[SensorConfigurations.format(COD)]
                for index in range(len(cod_data)):
                    if cod_data[index][SensorGetDeviceID[3:-3]] == self.deviceid:
                        check_con = check_con + 1
                        self.cod_reinitiliaze
                        del cod_data[index]
                        break
                if check_con == 0:
                    Datalogs().logging_error(BOD_Sensor_not_found.format(self.deviceid), SensorsError.format(COD))
                file_data[SensorConfigurations.format(COD)] = cod_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(COD))
            print("exception in remove_cod_configurations", ex)
            return ex
