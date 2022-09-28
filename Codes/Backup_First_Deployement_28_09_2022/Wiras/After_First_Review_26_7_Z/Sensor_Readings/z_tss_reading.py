"""
This document demonstrates function in relation with TSS Sensor
"""
import json
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
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r") as file:
            file_data = json.load(file)
            if 'TSS_Configurations' in file_data:
                for i in range(len(file_data["TSS_Configurations"])):
                    config_list.append(
                        list(file_data["TSS_Configurations"][i].values()))
                self.tss_configurations = config_list

    def check_error_message(self, sensor_reading, position):
        try:
            global connection_checking_count
            global sensor_result
            sensor_reading_check = str(sensor_reading)
            if sensor_reading_check == ErrorMessages[ModbusErrorMessage]:
                connection_checking_count = connection_checking_count+1
                if connection_checking_count == 10:
                    connection_checking_count = 0
                    sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                        TSS, position): self.tss_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(TSS, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                    TSS, position): self.tss_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(TSS, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(TSS, position): self.tss_configurations[position][0], SensorConfigurations[SensorGetData].format(
                    TSS): Conversion().parse_rawdata(sensor_reading.registers, self.tss_data_position[0], self.tss_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("tss_check_error_message::", ex)
            return ex

    def get_tss_reading(self):
        try:
            tss_data = {}
            for pos in range(len(self.tss_configurations)):
                while True:
                    tss_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tss_configurations[pos][2],
                        address=self.tss_configurations[pos][1],
                        unit=self.tss_configurations[pos][0]))
                    tss_data.update(self.check_error_message(tss_reading, pos))
                    if None not in tss_data.values():
                        break
            return tss_data
        except Exception as ex:
            print("get_cod_reading::", ex)
            return ex

    def set_tss_configurations(self, data):
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r+") as file:
            file_data = json.load(file)
            new_configuration = {"Device_ID": list(data.values())[0][0], "Start_Address": list(
                data.values())[0][1], "Register_Counts": list(data.values())[0][2]}
            file_data["TSS_Configurations"].append(new_configuration)
            unsorted_configuration = [dict(t) for t in {tuple(
                d.items()) for d in file_data["TSS_Configurations"]}]
            file_data["TSS_Configurations"] = sorted(
                unsorted_configuration, key=lambda i: i['Device_ID'])
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def set_slave_id(self, new_slave_id):
        try:
            with open("Configurations_and_Errors/Sensor_Addresses.json", 'r') as file:
                data = json.load(file)
                sensor_address = data["Device_Address"]["TSS_Start_Address"]
                sensor_id = data["Device_ID"]["TSS_Default_Id"]
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

