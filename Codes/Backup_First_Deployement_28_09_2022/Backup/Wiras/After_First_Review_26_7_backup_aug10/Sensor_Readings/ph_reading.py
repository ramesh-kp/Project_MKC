"""
This document demonstrates function in relation with PH Sensor
"""
import copy
import json
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from general_configurations import(
    MKC17,
    MKC21,
    MKC28,
    PH,
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


class PhSensor(object):
    """
    This class contain functions which initilize configurations of PH and its array position for getting the PH data
    from the PH reading.It contain functions which reads the data from PH Sensor.
    """

    def __init__(self):
        config_list = []
        self.ph_configurations = None
        self.ph_data_position = [2, 3]
        with open(Configurations_File, "r") as file:
            file_data = json.load(file)
            if SensorConfigurations.format(PH) in file_data:
                for i in range(len(file_data[SensorConfigurations.format(PH)])):
                    config_list.append(
                        list(file_data[SensorConfigurations.format(PH)][i].values()))
                self.ph_configurations = config_list

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
                        PH, position): self.ph_configurations[position][0],
                                          ErrorMessageSensor.format(PH, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ModbusSlaveIdErrorMessage:
                sensor_result.update({SensorGetDeviceID.format(
                    PH, position): self.ph_configurations[position][0],
                                      ErrorMessageSensor.format(PH, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorGetDeviceID.format(PH, position): self.ph_configurations[position][0],
                                      SensorGetData.format(
                    PH, position): Conversion().parse_rawdata(sensor_reading.registers,
                                                              self.ph_data_position[0], self.ph_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("ph_check_error_message::", ex)
            return {ErrorMessageSensor.format(
                        PH, position): ValidationError[MKC28]}

    def get_ph_reading(self):
        try:
            ph_data = {}
            for pos in range(len(self.ph_configurations)):
                while True:
                    ph_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.ph_configurations[pos][2],
                        address=self.ph_configurations[pos][1],
                        unit=self.ph_configurations[pos][0]))
                    ph_data.update(self.validate_content(ph_reading, pos))
                    if None not in ph_data.values():
                        break
            return ph_data
        except Exception as ex:
            print("get_ph_reading::", ex)
            return ({ErrorMessageSensor.format(
                        PH, pos): ValidationError[MKC28]})

    @classmethod
    def add_device(cls, new_slave_id):
        try:
            with open(Sensor_Address_File, 'r') as file:
                data = json.load(file)
                sensor_address = data[SensorGetAddress[3:-3]][SensorGetStartAddress[:-3].format(PH)]
                sensor_id = data[SensorGetDeviceID[3:-3]][SensorGetDefaultID[:-3].format(PH)]
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
    def set_ph_configurations(cls, data):
        with open(Configurations_File, "r+") as file:
            file_data = json.load(file)
            new_configuration = {SensorGetDeviceID[3:-3]: list(data.values())[0][0], SensorGetStartAddress[3:-3]: list(
                data.values())[0][1], SensorGetRegisterCounts[3:-3]: list(data.values())[0][2]}
            count = 0
            for position in range(len(file_data[SensorConfigurations.format(PH)])):
                if file_data[SensorConfigurations.format(PH)][position][SensorGetDeviceID[3:-3]] ==\
                    new_configuration[SensorGetDeviceID[3:-3]]:
                    count = count+1
                    print(Device_already_exists)
                # else:
                    # file_data[SensorConfigurations.format(PH)].append(new_configuration)
                    # unsorted_configuration = [dict(t) for t in {tuple(
                    #     d.items()) for d in file_data[SensorConfigurations.format(PH)]}]
                    # file_data[SensorConfigurations.format(PH)] = sorted(unsorted_configuration,
                    #                                                     key=lambda i: i[SensorGetDeviceID[3:-3]])
            if count == 0:
                file_data[SensorConfigurations.format(PH)].append(new_configuration)
                unsorted_configuration = [dict(t) for t in {tuple(
                    d.items()) for d in file_data[SensorConfigurations.format(PH)]}]
                file_data[SensorConfigurations.format(PH)] = sorted(unsorted_configuration,
                                                                        key=lambda i: i[SensorGetDeviceID[3:-3]])
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            # ########self.set_slave_id(new_configuration["Device_ID"])

    def ph_reinitiliaze(self, ph_flag_check):
            if ph_flag_check == True:
                self.ph_configurations = None
            else:
                print("ReIntilization unsucessful due to writing failed.")

    def remove_ph_configurations(self, device_id, ph_flag_check):
        try:
            check_con = 0
            with open(Configurations_File, "r+") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                ph_data = file_data_change[SensorConfigurations.format(PH)]
                for index in range(len(ph_data)):
                    if ph_data[index][SensorGetDeviceID[3:-3]] == device_id:
                        check_con = check_con + 1
                        self.ph_reinitiliaze(ph_flag_check)
                        del ph_data[index]
                        break
                if check_con == 0:
                    print("Ph DeviceID {} Not found".format(device_id))
                file_data[SensorConfigurations.format(PH)] = ph_data
                file.truncate(0)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except Exception as ex:
            Datalogs().logging_error(ex, SensorsError.format(PH))
            print("exception in remove_ph_configurations", ex)
            return ex
