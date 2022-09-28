"""
This document demonstrates function in relation with TDS Sensor
"""
import copy
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC28,
    TDS,
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


class TDSSensor(object):
    """
    This class contain functions which initilize configurations of TDS and its array position for getting the TDS data
    from the TDS reading.It contain functions which reads the data from TDS Sensor.
    """

    def __init__(self):
        config_list = []
        self.tds_configurations = None
        self.tds_data_position = [2, 3]
        with open(Configurations_File, "r") as file:
            file_data = json.load(file)
            if SensorConfigurations.format(TDS) in file_data:
                for i in range(len(file_data[SensorConfigurations.format(TDS)])):
                    config_list.append(
                        list(file_data[SensorConfigurations.format(TDS)][i].values()))
                self.tds_configurations = config_list

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
                        TDS, position): self.tds_configurations[position][0],
                        ErrorMessageSensor.format(TDS, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(
                    TDS, position): self.tds_configurations[position][0],
                    ErrorMessageSensor.format(TDS, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(TDS, position): self.tds_configurations[position][0],
                                      SensorGetData.format(
                    TDS, position): Conversion().parse_rawdata(sensor_reading.registers, self.tds_data_position[0],
                                                               self.tds_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("tds_check_error_message::", ex)
            return {ErrorMessageSensor.format(TDS, position): ValidationError[MKC28]}

    def get_tds_reading(self):
        try:
            tds_data = {}
            for pos in range(len(self.tds_configurations)):
                while True:
                    tds_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tds_configurations[pos][2],
                        address=self.tds_configurations[pos][1],
                        unit=self.tds_configurations[pos][0]))
                    tds_data.update(self.validate_content(tds_reading, pos))
                    if None not in tds_data.values():
                        break
            return tds_data
        except Exception as ex:
            print("get_tds_reading::", ex)
            return ({ErrorMessageSensor.format(
                        TDS, pos): ValidationError[MKC28]})

    @classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]
                                      ][SensorGetStartAddress[:-3].format(TDS)]
                sensor_id = data[SensorGetDeviceID[3:-3]
                                 ][SensorGetDefaultID[:-3].format(TDS)]
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
    def set_tds_configurations(cls, data):
        with open(Configurations_File, "r+") as file:
            file_data = json.load(file)
            new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0], SensorGetStartAddress[3:-3]: list(
                data.values())[0][1], SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
            count = 0
            for position in range(len(file_data[SensorConfigurations.format(TDS)])):
                if file_data[SensorConfigurations.format(TDS)][position][SensorGetDeviceID[3:-3]] ==\
                    new_configuration[SensorGetDeviceID[3:-3]]:
                    count = count+1
                    print(Device_already_exists)
                # else:
                #     file_data[SensorConfigurations.format(
                #         TDS)].append(new_configuration)
                #     unsorted_configuration = [dict(t) for t in {tuple(
                #         d.items()) for d in file_data[SensorConfigurations.format(TDS)]}]
                #     file_data[SensorConfigurations.format(TDS)] = sorted(
                #         unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
            if count == 0:
                file_data[SensorConfigurations.format(
                        TDS)].append(new_configuration)
                unsorted_configuration = [dict(t) for t in {tuple(
                    d.items()) for d in file_data[SensorConfigurations.format(TDS)]}]
                file_data[SensorConfigurations.format(TDS)] = sorted(
                    unsorted_configuration, key=lambda i: i[SensorGetDeviceID[3:-3]])
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            # ########self.set_slave_id(new_configuration["Device_ID"])

    def tds_reinitiliaze(self, tds_flag_check):
        if tds_flag_check == True:
            self.tds_configurations = None
        else:
            print("ReIntilization unsucessful due to writing failed.")

    def remove_tds_configurations(self, device_id, tds_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                tds_data = file_data_change[SensorConfigurations.format(TDS)]
                for index in range(len(tds_data)):
                    if tds_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.tds_reinitiliaze(tds_flag_check)
                        del tds_data[index]
                        break
                if check_con == 0:
                    print("TDS DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(TDS)] = tds_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(TDS))
            print("exception in remove_tds_configurations", ex)
            return ex
