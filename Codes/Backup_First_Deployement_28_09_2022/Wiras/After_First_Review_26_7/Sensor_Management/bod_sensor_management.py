'''
This document demonstrates function in relation with BOD Sensor
'''
import copy
import json

from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from Utilities.util_error_mapping import Matching

from general_configurations import bod_position_1, bod_position_2, flag_status_0, BOD
from general_configurations import Configurations_File, read_mode
from general_configurations import INFO_NOT_FOUND_IN_FILE, indent_level, increment_1
from general_configurations import Added_device_successfully, BOD_Sensor_not_found
from general_configurations import Configurations_added_successfully, count_0
from general_configurations import INVALID_CONFIGURATIONS, INVALID_DATA_FROM_MODBUS
from general_configurations import INVALID_INFO, INVALID_SLAVE_ID, Error_Code_Formatter
from general_configurations import Configurations_removed_successfully, Debug, Error
from general_configurations import ErrorMessageSensor, Log_levels, Unable_to_add_Device
from general_configurations import SensorGetDefaultID, initial_index, index_position_2
from general_configurations import (
    Error_in_enable_reading,
    Error_in_set_bod_configurations,
)
from general_configurations import (
    Info,
    New_configurations_added_to_file,
    Reading_disabled,
)
from general_configurations import ModbusErrorMessage, ModbusSlaveIdErrorMessage
from general_configurations import (
    Received_readings_from_Sensor,
    SensorGetData,
    SensorGetDeviceID,
)
from general_configurations import (
    SensorsError,
    SensorConfigurations,
    SensorGetStartAddress,
)
from general_configurations import SensorGetRegisterCounts, Device_already_exists
from general_configurations import (
    Sensor_Address_File,
    SensorGetAddress,
    read_write_mode,
)
from general_configurations import array_position_0, array_position_1, array_position_2
from general_configurations import final_index, index_position_0, index_position_1
from general_configurations import (
    postion_0,
    flag_status_1,
    connection_count_0,
    connection_count_10,
    bod_array_pos_1,
    bod_array_pos_2
)

from logging_info import Datalogs


# connection_checking_count = connection_count_0



class BODSensor(object):
    """
    This class contain functions which initilize configurations of BOD and its array position
    for getting the BOD data from the BOD reading.It contain functions which reads the data from
    BOD Sensor.
    """
    ModbusError = ModbusErrorMessage
    ModbusSlaveIdError = ModbusSlaveIdErrorMessage

    def __init__(self,deviceid = None):
        self.deviceid = deviceid
        self.bod_start_flag = flag_status_0
        self.bod_configurations = None
        self.bod_data_position = [bod_array_pos_1, bod_array_pos_2]
        self.bod_configurations = self.get_bod_configurations()
    def get_bod_configurations(self):
        """
        Description: Returns the bod configurations from Sensor_Configuration_File.
        Input Parameters: None
        Output Type: list
        """

        try:
            config_list = []
            with open(Configurations_File, read_mode, encoding="utf-8") as file:
                file_data = json.load(file)
                if file_data and SensorConfigurations.format(BOD) in file_data:
                    for position in range(len(file_data[SensorConfigurations.format(BOD)])):
                        config_list.append(
                            list(file_data[SensorConfigurations.format(BOD)][position].values()))
                    self.bod_configurations = config_list
                    result =  config_list
                else:
                    result =  None
                    Datalogs().logging_error(Matching().error_mapping(INFO_NOT_FOUND_IN_FILE),
                            SensorsError.format(BOD,self.deviceid), Log_levels[Debug])
                return result
        except FileNotFoundError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD,self.deviceid),
                                                  Log_levels[Error])
            return ex
        except AttributeError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD,self.deviceid),
                                                  Log_levels[Error])

    def validate_message(self, message):
        """
        Description: Returns the Matching error if there is an error from the sensor
        Input Parameters: output from sensor
        Output Type: string

        """
        connection_checking_count = connection_count_0
        match message:
            case self.ModbusError:
                connection_checking_count = connection_checking_count+increment_1
                if connection_checking_count == connection_count_10:
                    result = Matching().error_mapping(INVALID_DATA_FROM_MODBUS)
                else:
                    result = None
                return result
            case self.ModbusSlaveIdError:
                return Matching().error_mapping(INVALID_SLAVE_ID)

    def validate_content(self, sensor_reading, position):
        """
        Description: Returns the Output from sensor in the required format.
        Input Parameters: sensor readings and the position of the sensor from the
        configuration list
        Output Type: dictionary

        """
        try:
            sensor_result = {}
            sensor_reading_check = str(sensor_reading)
            if self.validate_message(sensor_reading_check):
                result = self.validate_message(sensor_reading_check)
                sensor_result.update({SensorGetDeviceID.format(BOD, position):
                    self.bod_configurations[position][array_position_0],
                    ErrorMessageSensor.format(BOD, position): result})
            else:
                sensor_result.update({SensorGetDeviceID.format(BOD, position):
                    self.bod_configurations[position][array_position_0],
                    SensorGetData.format(BOD, position): Conversion().parse_rawdata(
                        sensor_reading.registers,self.bod_data_position[bod_position_1],
                        self.bod_data_position[bod_position_2])})
            return sensor_result
        except IndexError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD,self.deviceid),
                                                Log_levels[Error])
        # except Exception as ex:
        #     Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD,self.deviceid),
        #                                         Log_levels[Error])
            # return {ErrorMessageSensor.format(BOD, position):
            #     Matching().error_mapping(CONNECTION_FAILED)}

    def get_bod_reading(self, bod_start_flag):
        """
        Description: Returns the final output from the sensor readings
        Input Parameters: bod_start_flag which is either True or False
        Output Type: dictionary
        """
        try:
            bod_data = {}
            for position, _ in enumerate(self.bod_configurations):
                while True:
                    if (bod_start_flag == flag_status_1) and (self.deviceid ==
                                self.bod_configurations[position][array_position_0]):
                        bod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                            count=self.bod_configurations[position][array_position_2],
                            address=self.bod_configurations[position][array_position_1],
                            unit=self.bod_configurations[position][array_position_0]))
                        bod_data.update(self.validate_content(bod_reading, position))
                        Datalogs.get_instance().logging_error(Received_readings_from_Sensor,
                                    SensorsError.format(BOD, self.deviceid), Log_levels[Info])
                        if None not in bod_data.values():
                            break
                    else:
                        break
            return bod_data
        except IndexError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                  Log_levels[Error])
            return {ErrorMessageSensor.format(BOD, self.deviceid):ex}

    def enable_reading(self):
        """
        Description: Returns the sensor readings by pass the True flag
        Input Parameters: None
        Output Type: dictionary
        """
        try:
            if self.bod_configurations is not None:
                self.bod_start_flag = flag_status_1
                result = self.get_bod_reading(self.bod_start_flag)
            else:
                result = Matching().error_mapping(INVALID_CONFIGURATIONS)
                print(result)
                Datalogs.get_instance().logging_error((Error_Code_Formatter.format(Matching(
                    ).error_mapping(INVALID_CONFIGURATIONS), Error_in_enable_reading)),
                        SensorsError.format(BOD, self.deviceid), Log_levels[Error])
            return {BOD:result}
        except IndexError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                  Log_levels[Error])
            return ex

    def diasble_reading(self):
        """
        Description: Disables the sensor readings by setting the flag to False
        Input Parameters: None
        Output Type: string
        """
        try:
            self.bod_start_flag = flag_status_0
            self.get_bod_reading(self.bod_start_flag)
            Datalogs.get_instance().logging_error(Reading_disabled,SensorsError.format(
                BOD, self.deviceid), Log_levels[Info])
            return Reading_disabled
        except IndexError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                  Log_levels[Error])
            return ex

    @classmethod
    def add_device(cls, new_slave_id):
        """
        Description: set new device id to the sensors
        Input Parameters: new_slave_id
        Output Type: string
        """
        try:
            res = None
            count = 0
            while count < 3:
                with open(Sensor_Address_File, read_mode, encoding="utf-8") as file:
                    data = json.load(file)
                    sensor_address = data[SensorGetAddress[initial_index:final_index]
                                        ][SensorGetStartAddress[:final_index].format(BOD)]
                    sensor_id = data[SensorGetDeviceID[initial_index:final_index]
                                    ][SensorGetDefaultID[:final_index].format(BOD)]
                    res = DeviceCommunication().gateway_connect().write_registers(
                        address=sensor_address,
                        values=Conversion().little_to_big_endian(new_slave_id),
                        unit=int(sensor_id))
                    if res is None:
                        count = count+1
                    else:
                        result = Added_device_successfully
                        break
                    # address - Starting Address
                    # values - Values to write
                    # unit - Current Slave Id
                    print(res)
                    Datalogs.get_instance().logging_error(Added_device_successfully,
                                    SensorsError.format(BOD), Log_levels[Info])
                    result = Added_device_successfully
            if count >= 3:
                result = Unable_to_add_Device
            return {BOD:result}
        except FileNotFoundError as ex:
            print("999",ex.errno)
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD), Log_levels[Debug])
            return ex


    def set_bod_configurations(self, data):
        """
        Description: Add device to the sensor configurations file
        Input Parameters: configurations to be added
        Output Type: string
        """
        try:
            with open(Configurations_File, read_write_mode, encoding="utf-8") as file:
                file_data = json.load(file)
                if list((data).keys())[index_position_0] == BOD:
                    new_configuration = {SensorGetDeviceID[initial_index:final_index]: list(
                        data.values())[index_position_0][index_position_0],
                                        SensorGetStartAddress[initial_index:final_index]: list(
                                            data.values())[index_position_0][index_position_1],
                                        SensorGetRegisterCounts[initial_index:final_index]: list(
                                            data.values())[index_position_0][index_position_2]}
                    count = count_0
                    for position in range(len(file_data[SensorConfigurations.format(BOD)])):
                        if file_data[SensorConfigurations.format(BOD)][position][SensorGetDeviceID[
                            initial_index:final_index]] == new_configuration[SensorGetDeviceID
                                                            [initial_index:final_index]]:
                            count = count+increment_1
                            result = Device_already_exists
                    if count == count_0:
                        file_data[SensorConfigurations.format(
                            BOD)].append(new_configuration)
                        unsorted_configuration = [dict(t) for t in {tuple(
                            d.items()) for d in file_data[SensorConfigurations.format(BOD)]}]
                        file_data[SensorConfigurations.format(BOD)] = sorted(
                            unsorted_configuration, key=lambda i:
                                i[SensorGetDeviceID[initial_index:final_index]])
                        file.truncate(postion_0)
                        file.seek(postion_0)
                        json.dump(file_data, file, indent=indent_level)
                        Datalogs.get_instance().logging_error(Configurations_added_successfully,
                                    SensorsError.format(BOD, self.deviceid),Log_levels[Info])
                    # ########self.set_slave_id(new_configuration[SensorGetDeviceID[initial_index:final_index]])
                        result = New_configurations_added_to_file
                else:
                    Datalogs.get_instance().logging_error((Error_Code_Formatter.format(
                        INVALID_INFO, Error_in_set_bod_configurations)),SensorsError.format(
                            BOD, self.deviceid), Log_levels[Error])
                    result = Matching().error_mapping(INVALID_INFO)
                return {BOD:result}
        except FileNotFoundError as ex:
            print("1000",ex.errno)
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                  Log_levels[Error])
            return ex
        except IndexError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                  Log_levels[Error])
            return ex

    def bod_reinitiliaze(self):
        """
        Description: Reinitiazes the sensor
        Input Parameters: None
        Output Type: string
        """
        try:
            self.diasble_reading()
            self.bod_configurations = None
        except ValueError as ex:
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                Log_levels[Error])
            return ex

    def remove_bod_configurations(self):
        """
        Description: Removes the configurations the sensor configurations file
        Input Parameters: None
        Output Type: string
        """
        try:
            check_con = count_0
            with open(Configurations_File, read_write_mode, encoding="utf-8") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                bod_data = file_data_change[SensorConfigurations.format(BOD)]
                for index, _ in enumerate(len(bod_data)):
                    if bod_data[index][SensorGetDeviceID[initial_index:final_index]
                                       ] == self.deviceid:
                        check_con = check_con + increment_1
                        self.bod_reinitiliaze()
                        del bod_data[index]
                        result = Configurations_removed_successfully
                if check_con == count_0:
                    Datalogs.get_instance().logging_error(BOD_Sensor_not_found.format(
                        self.deviceid), SensorsError.format(BOD, self.deviceid),
                                                        Log_levels[Error])
                    result = BOD_Sensor_not_found.format(self.deviceid)
                file_data[SensorConfigurations.format(BOD)] = bod_data
                file.truncate(postion_0)
                file.seek(postion_0)
                json.dump(file_data, file, indent = indent_level)
            return result
        except FileNotFoundError as ex:
            print("156565",ex.errno)
            Datalogs.get_instance().logging_error(ex, SensorsError.format(BOD, self.deviceid),
                                                  Log_levels[Error])
            return ex
