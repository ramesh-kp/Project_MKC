"""
This document demonstrates function in relation with TSS Sensor
"""
import copy
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC28,
    TSS,
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


class TSSSensor(object):
    """
    This class contain functions which initilize configurations of TSS and its array position for getting the TSS data
    from the TSS reading.It contain functions which reads the data from TSS Sensor.
    """

    def __init__(self):
        config_list = []
        self.tss_configurations = None
        self.tss_data_position = [0, 1]
        with open(Configurations_File, "r") as file:
            file_data = json.load(file)
            if SensorConfigurations.format(TSS) in file_data:
                for i in range(len(file_data[SensorConfigurations.format(TSS)])):
                    config_list.append(
                        list(file_data[SensorConfigurations.format(TSS)][i].values()))
                self.tss_configurations = config_list

    def validate_content(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ModbusErrorMessage:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorGetDeviceID.format(
                        TSS, position): self.tss_configurations[position][0],
                        ErrorMessageSensor.format(TSS, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(
                    TSS, position): self.tss_configurations[position][0],
                    ErrorMessageSensor.format(TSS, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(TSS, position): self.tss_configurations[position][0],
                                      SensorGetData.format(
                    TSS, position): Conversion().parse_rawdata(sensor_reading.registers,
                                                               self.tss_data_position[0], self.tss_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("tss_check_error_message::", ex)
            return {ErrorMessageSensor.format(
                        TSS, position): ValidationError[MKC28]}

    def get_tss_reading(self):
        try:
            tss_data = {}
            for pos in range(len(self.tss_configurations)):
                while True:
                    tss_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tss_configurations[pos][2],
                        address=self.tss_configurations[pos][1],
                        unit=self.tss_configurations[pos][0]))
                    tss_data.update(self.validate_content(tss_reading, pos))
                    if None not in tss_data.values():
                        break
            return tss_data
        except Exception as ex:
            print("get_cod_reading::", ex)
            return ({ErrorMessageSensor.format(
                        TSS, pos): ValidationError[MKC28]})

    @classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]
                                      ][SensorGetStartAddress[:-3].format(TSS)]
                sensor_id = data[SensorGetDeviceID[3:-3]
                                 ][SensorGetDefaultID[:-3].format(TSS)]
                res = DeviceCommunication().gateway_connect().write_registers(
                    address=sensor_address,
                    values=Conversion().little_to_big_endian(new_slave_id),
                    unit=int(sensor_id))
                # address - Starting Address
                # values - Values to write
                # unit - Current Slave Id
                print(res)
        except Exception as e:
            print(e)

    @classmethod
    def set_tss_configurations(cls, data):
        with open(Configurations_File, "r+") as file:
            file_data = json.load(file)
            new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0], SensorGetStartAddress[3:-3]: list(
                data.values())[0][1], SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
            count = 0
            for position in range(len(file_data[SensorConfigurations.format(TSS)])):
                if file_data[SensorConfigurations.format(TSS)][position][SensorGetDeviceID[3:-3]] ==\
                        new_configuration[SensorGetDeviceID[3:-3]]:
                    count = count+1
                    print(Device_already_exists)
                # else:
                    # file_data[SensorConfigurations.format(
                    #     TSS)].append(new_configuration)
                    # unsorted_configuration = [dict(t) for t in {tuple(
                    #     d.items()) for d in file_data[SensorConfigurations.format(TSS)]}]
                    # file_data[SensorConfigurations.format(TSS)] = sorted(unsorted_configuration,
                    #                                                      key=lambda i: i[SensorGetDeviceID[3:-3]])
            if count == 0:
                file_data[SensorConfigurations.format(
                        TSS)].append(new_configuration)
                unsorted_configuration = [dict(t) for t in {tuple(
                    d.items()) for d in file_data[SensorConfigurations.format(TSS)]}]
                file_data[SensorConfigurations.format(TSS)] = sorted(unsorted_configuration,
                                                                        key=lambda i: i[SensorGetDeviceID[3:-3]])
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            # ########self.set_slave_id(new_configuration["Device_ID"])

    def tss_reinitiliaze(self, tss_flag_check):
        if tss_flag_check == True:
            self.tss_configurations = None
        else:
            print("ReIntilization unsucessful due to writing failed.")

    def remove_tss_configurations(self, device_id, tss_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                tss_data = file_data_change[SensorConfigurations.format(TSS)]
                for index in range(len(tss_data)):
                    if tss_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.tss_reinitiliaze(tss_flag_check)
                        del tss_data[index]
                        break
                if check_con == 0:
                    print("TSS DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(TSS)] = tss_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(TSS))
            print("exception in remove_tss_configurations", ex)
            return ex
