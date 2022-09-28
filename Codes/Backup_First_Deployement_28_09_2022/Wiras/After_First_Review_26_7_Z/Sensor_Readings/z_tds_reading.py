"""
This document demonstrates function in relation with TDS Sensor
"""
import json
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
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r") as file:
            file_data = json.load(file)
            if 'TDS_Configurations' in file_data:
                for i in range(len(file_data["TDS_Configurations"])):
                    config_list.append(
                        list(file_data["TDS_Configurations"][i].values()))
                self.tds_configurations = config_list


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
                        TDS, position): self.tds_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(TDS, position): ValidationError[MKC17]})
                else:
                    sensor_result.update({"None": None})
            elif sensor_reading_check == ErrorMessages[ModbusSlaveIdErrorMessage]:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(
                    TDS, position): self.tds_configurations[position][0], ErrorMessages[ErrorMessageSensor].format(TDS, position): ValidationError[MKC21]})
            else:
                sensor_result.update({SensorConfigurations[SensorGetDeviceID].format(TDS, position): self.tds_configurations[position][0], SensorConfigurations[SensorGetData].format(
                    TDS): Conversion().parse_rawdata(sensor_reading.registers, self.tds_data_position[0], self.tds_data_position[1])})
            return sensor_result
        except Exception as ex:
            print("tds_check_error_message::", ex)
            return ex

    def get_tds_reading(self):
        try:
            tds_data = {}
            for pos in range(len(self.tds_configurations)):
                while True:
                    tds_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tds_configurations[pos][2],
                        address=self.tds_configurations[pos][1],
                        unit=self.tds_configurations[pos][0]))
                    tds_data.update(self.check_error_message(tds_reading, pos))
                    if None not in tds_data.values():
                        break
            return tds_data
        except Exception as ex:
            print("get_tds_reading::", ex)
            return ex

    def set_tds_configurations(self, data):
        with open("Configurations_and_Errors/Sensor_Configurations.json", "r+") as file:
            file_data = json.load(file)
            new_configuration = {"Device_ID": list(data.values())[0][0], "Start_Address": list(
                data.values())[0][1], "Register_Counts": list(data.values())[0][2]}
            file_data["TDS_Configurations"].append(new_configuration)
            unsorted_configuration = [dict(t) for t in {tuple(
                d.items()) for d in file_data["TDS_Configurations"]}]
            file_data["TDS_Configurations"] = sorted(
                unsorted_configuration, key=lambda i: i['Device_ID'])
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def set_slave_id(self, new_slave_id):
        try:
            with open("Configurations_and_Errors/Sensor_Addresses.json", 'r') as file:
                data = json.load(file)
                sensor_address = data["Device_Address"]["TDS_Start_Address"]
                sensor_id = data["Device_ID"]["TDS_Default_Id"]
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
