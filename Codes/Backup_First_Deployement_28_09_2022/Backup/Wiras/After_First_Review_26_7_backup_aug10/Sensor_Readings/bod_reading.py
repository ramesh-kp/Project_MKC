"""
This document demonstrates function in relation with BOD Sensor
"""
import copy
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    BOD,
    MKC17,
    MKC21,
    MKC28,
    ErrorMessageSensor,
    ModbusErrorMessage,
    ModbusSlaveIdErrorMessage,
    SensorGetData,
    SensorGetDeviceID,
    SensorsError,
    ValidationError,
    SensorConfigurations,
    SensorGetStartAddress,
    SensorGetDefaultID,
    SensorGetRegisterCounts,
    Device_already_exists,
    Configurations_File,
    Sensor_Address_File,
    SensorGetAddress)
from logging_info import Datalogs


connection_checking_count = 0
sensor_result = {}
bod_start_flag = True


class BODSensor(object):
    """
    This class contain functions which initilize configurations of BOD and its array position for getting the BOD data
    from the BOD reading.It contain functions which reads the data from BOD Sensor.
    """

    def __init__(self):
        try:
            config_list = []
            self.bod_configurations = None
            self.bod_data_position = [2, 3]
            with open(Configurations_File, "r") as file:
                file_data = json.load(file)
                if SensorConfigurations.format(BOD) in file_data:
                    for i in range(len(file_data[SensorConfigurations.format(BOD)])):
                        config_list.append(
                            list(file_data[SensorConfigurations.format(BOD)][i].values()))
                    self.bod_configurations = config_list
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(BOD))

    def validate_content(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ModbusErrorMessage:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorGetDeviceID.format(BOD, position): self.bod_configurations[position][0],
                                          ErrorMessageSensor.format(BOD, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(BOD, position): self.bod_configurations[position][0],
                                      ErrorMessageSensor.format(BOD, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(BOD, position): self.bod_configurations[position][0],
                                      SensorGetData.format(BOD, position): Conversion().parse_rawdata(
                    sensor_reading.registers, self.bod_data_position[0], self.bod_data_position[1])})
            return sensor_result
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(BOD))
            print("bod_check_error_message::", ex)
            return {ErrorMessageSensor.format(
                        BOD, position):ValidationError[MKC28]}


    def get_bod_reading(self, bod_start_flag):
        try:
            bod_data = {}
            for pos in range(len(self.bod_configurations)):
                while bod_start_flag:
                    bod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.bod_configurations[pos][2],
                        address=self.bod_configurations[pos][1],
                        unit=self.bod_configurations[pos][0]))
                    bod_data.update(self.validate_content(bod_reading, pos))
                    if None not in bod_data.values():
                        break
            return bod_data
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(BOD))
            print("get_bod_reading::", ex)
            return ({ErrorMessageSensor.format(
                        BOD, pos): ValidationError[MKC28]})

    @classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]
                                      ][SensorGetStartAddress[:-3].format(BOD)]
                sensor_id = data[SensorGetDeviceID[3:-3]
                                 ][SensorGetDefaultID[:-3].format(BOD)]
                res = DeviceCommunication().gateway_connect().write_registers(
                    address=sensor_address,
                    values=Conversion().little_to_big_endian(new_slave_id),
                    unit=int(sensor_id))
                # address - Starting Address
                # values - Values to write
                # unit - Current Slave Id
                print(res)
        except Exception as e:
            print("add_device_in_bod::", e)

    @classmethod
    def set_bod_configurations(cls, data):
        try:
            with open(Configurations_File, "r+") as file:
                file_data = json.load(file)
                new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0],
                                     SensorGetStartAddress[3:-3]: list(data.values())[0][1],
                                     SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
                count = 0
                for position in range(len(file_data[SensorConfigurations.format(BOD)])):
                    if file_data[SensorConfigurations.format(BOD)][position][SensorGetDeviceID[3:-3]] == \
                            new_configuration[SensorGetDeviceID[3:-3]]:
                        count = count+1
                        print(Device_already_exists)
                if count == 0:
                    file_data[SensorConfigurations.format(
                            BOD)].append(new_configuration)
                    unsorted_configuration = [dict(t) for t in {tuple(
                        d.items()) for d in file_data[SensorConfigurations.format(BOD)]}]
                    file_data[SensorConfigurations.format(BOD)] = sorted(
                        unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
                    file.truncate(0)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                # ########self.set_slave_id(new_configuration[SensorGetDeviceID[3:-3]])
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(BOD))

    def bod_reinitiliaze(self, bod_flag_check):
        global bod_start_flag
        bod_start_flag = False
        if bod_flag_check == True:
            self.bod_configurations = None
        else:
            print("ReIntilization unsucessful due to writing failed.")

    def remove_bod_configurations(self, device_id, bod_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                bod_data = file_data_change[SensorConfigurations.format(BOD)]
                for index in range(len(bod_data)):
                    if bod_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.bod_reinitiliaze(bod_flag_check)
                        del bod_data[index]
                        break
                if check_con == 0:
                    print("BOD DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(BOD)] = bod_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(BOD))
