"""
This document demonstrates function in connection with Energymeter sensor
"""
import json
import copy
from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_error_mapping import Matching
from general_configurations import ARRAY_POSITION_0, ARRAY_POSITION_1, ARRAY_POSITION_2
from general_configurations import ATTRIBUTEERROR, CONFIGURATIONS_ADDED_SUCCESSFULLY
from general_configurations import CONFIGURATIONS_FILE, CONFIGURATIONS_REMOVED_SUCCESSFULLY
from general_configurations import ENERGYMETER_SENSOR_NOT_FOUND, CONNECTION_COUNT_0
from general_configurations import CONNECTION_COUNT_10, COUNT_0, DEBUG, ERROR
from general_configurations import DEVICE_ALREADY_EXISTS, ENERGYMETER
from general_configurations import ERROR_CODE_FORMATTER, ERROR_IN_ENABLE_READING
from general_configurations import ERROR_IN_SET_ENERGYMETER_CONFIGURATIONS
from general_configurations import ERRORMESSAGESENSOR, FILENOTFOUND, FINAL_INDEX
from general_configurations import FLAG_STATUS_1, INCREMENT_1, INDENT_LEVEL
from general_configurations import INDEX_POSITION_0, INDEX_POSITION_1
from general_configurations import INDEX_POSITION_2, INDEXERROR, INFO
from general_configurations import INFO_NOT_FOUND_IN_FILE, INITIAL_INDEX
from general_configurations import INVALID_CONFIGURATIONS, INVALID_DATA_FROM_MODBUS
from general_configurations import INVALID_INFO, INVALID_SLAVE_ID
from general_configurations import MODBUSERRORMESSAGE, MODBUSSLAVEIDERRORMESSAGE
from general_configurations import NEW_CONFIGURATIONS_ADDED_TO_FILE
from general_configurations import POSTION_0, READ_MODE, READ_WRITE_MODE
from general_configurations import READING_DISABLED, RECEIVED_READINGS_FROM_SENSOR
from general_configurations import SENSORCONFIGURATIONS, SENSORGETDATA, SENSORGETDEVICEID
from general_configurations import SENSORGETREGISTERCOUNTS, SENSORGETSTARTADDRESS
from general_configurations import SENSORSERROR, VALUEERROR, ENERGYMETERCKWH, ENERGYMETERDEVICEID
from general_configurations import ENERGYMETERFREQUENCY, ENERGYMETERPOWERFACTORLINE1
from general_configurations import ENERGYMETERPOWERFACTORLINE2, ENERGYMETERPOWERFACTORLINE3
from general_configurations import ENERGYMETERTOTALPOWERFACTOR, ENERGYMETERVOLTAGE, FLAG_STATUS_0
from general_configurations import Error_number, Log_levels, ENERGYMETERCKAH
from general_configurations import CONNECTIONEXCEPTION, MODBUSCONNECTIONERROR

from logging_info import Datalogs



class EnergymeterSensor(object):
    """
    This class consist of functions in relation with the Energymeter Sensor.
    """

    modbuserror = MODBUSERRORMESSAGE
    modbusslaveiderror = MODBUSSLAVEIDERRORMESSAGE

    def __init__(self,deviceid = None):
        self.deviceid = deviceid
        self.energymeter_start_flag = FLAG_STATUS_0
        self.energymeter_configurations = None
        self.energymeter_configurations = self.get_energymeter_configurations()

    def get_energymeter_configurations(self):
        """
        Description: Returns the energymeter configurations from Sensor_Configuration_File.
        Input Parameters: None
        Output Type: list
        """

        try:
            config_list = []
            with open(CONFIGURATIONS_FILE, READ_MODE, encoding="utf-8") as file:
                file_data = json.load(file)
                if file_data and SENSORCONFIGURATIONS.format(ENERGYMETER) in file_data:
                    for position in range(len(file_data[SENSORCONFIGURATIONS.format(ENERGYMETER)])):
                        config_list.append(
                            list(file_data[SENSORCONFIGURATIONS.format(
                                ENERGYMETER)][position].values()))
                    self.energymeter_configurations = config_list
                    result =  config_list
                else:
                    result =  None
                    Datalogs().logging_error(Matching().error_mapping(INFO_NOT_FOUND_IN_FILE),
                            SENSORSERROR.format(ENERGYMETER, self.deviceid),
                            Log_levels[DEBUG],self.deviceid)
                return result
        except FileNotFoundError as ex:
            Datalogs.get_instance().logging_error((ex, Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex
        except AttributeError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[ATTRIBUTEERROR]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)

    @classmethod
    def parse_rawdata_energymeter(cls, energymeter_reading_raw, position):
        """
        Description: Returns the energymeter data from the readingsfrom the sensor
        Input Parameters: Ouput from the sensor
        Output Type: dictionary
        """
        try:
            slave_id = energymeter_reading_raw[1]
            ckwh = energymeter_reading_raw[5] / 1000
            ckah = energymeter_reading_raw[7] / 1000
            voltage = energymeter_reading_raw[9] / 10
            power_factor_line_1 = energymeter_reading_raw[33] / 100
            power_factor_line_2 = energymeter_reading_raw[35] / 100
            power_factor_line_3 = energymeter_reading_raw[37] / 100
            total_power_factor = energymeter_reading_raw[43] / 100
            frequency = energymeter_reading_raw[45] / 10
            energy_meter_data = {
                ENERGYMETERDEVICEID.format(position): slave_id,
                ENERGYMETERCKWH.format(position): ckwh,
                ENERGYMETERCKAH.format(position): ckah,
                ENERGYMETERVOLTAGE.format(position): voltage,
                ENERGYMETERPOWERFACTORLINE1.format(position): power_factor_line_1,
                ENERGYMETERPOWERFACTORLINE2.format(position): power_factor_line_2,
                ENERGYMETERPOWERFACTORLINE3.format(position): power_factor_line_3,
                ENERGYMETERTOTALPOWERFACTOR.format(position): total_power_factor,
                ENERGYMETERFREQUENCY.format(position): frequency,
            }
            return energy_meter_data
        except Exception as ex:
            return ex

    def validate_message(self, message):
        """
        Description: Returns the Matching error if there is an error from the sensor
        Input Parameters: output from sensor
        Output Type: string

        """
        connection_checking_count = CONNECTION_COUNT_0
        match message:
            case self.modbuserror:
                connection_checking_count = connection_checking_count+INCREMENT_1
                if connection_checking_count == CONNECTION_COUNT_10 :
                    result = Matching().error_mapping(INVALID_DATA_FROM_MODBUS)
                else:
                    result = None
                return result
            case self.modbusslaveiderror:
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
                sensor_result.update({SENSORGETDEVICEID.format(ENERGYMETER, position):
                    self.energymeter_configurations[position][ARRAY_POSITION_0 ],
                    ERRORMESSAGESENSOR.format(ENERGYMETER, position): result})
            else:
                sensor_result.update({SENSORGETDEVICEID.format(ENERGYMETER, position):
                    self.energymeter_configurations[position][ARRAY_POSITION_0 ],
                    SENSORGETDATA.format(ENERGYMETER, position): self.parse_rawdata_energymeter(
                    sensor_reading.registers, position)})
            return sensor_result
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex, Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(ENERGYMETER,self.deviceid),
                                                Log_levels[ERROR], self.deviceid)
            return ex


    def get_energymeter_reading(self, energymeter_start_flag):
        """
        Description: Returns the final output from the sensor readings
        Input Parameters: energymeter_start_flag which is either True or False
        Output Type: dictionary
        """
        try:
            energymeter_data = {}
            for position, _ in enumerate(self.energymeter_configurations):
                while True:
                    if (energymeter_start_flag == FLAG_STATUS_1) and (self.deviceid ==
                                self.energymeter_configurations[position][ARRAY_POSITION_0 ]):
                        energymeter_reading = (DeviceCommunication.gateway_connect(
                            ).read_holding_registers(count = self.energymeter_configurations[
                                position][ARRAY_POSITION_2],
                            address = self.energymeter_configurations[position][ARRAY_POSITION_1 ],
                            unit = self.energymeter_configurations[position][ARRAY_POSITION_0]))
                        energymeter_data.update(self.validate_content(energymeter_reading,
                                                                      position))
                        Datalogs.get_instance().logging_error(RECEIVED_READINGS_FROM_SENSOR,
                                    SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                    Log_levels[INFO], self.deviceid)
                        if None not in energymeter_data.values():
                            break
                    else:
                        break
            return energymeter_data
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex, Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return {ERRORMESSAGESENSOR.format(ENERGYMETER, self.deviceid):ex}
        except Exception as ex:
            if type(ex).__name__ == CONNECTIONEXCEPTION:
                result = {ERRORMESSAGESENSOR.format(ENERGYMETER, self.deviceid):
                    MODBUSCONNECTIONERROR}
            else:
                result = {ERRORMESSAGESENSOR.format(ENERGYMETER, self.deviceid):ex}
            Datalogs.get_instance().logging_error(ex,
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return result

    def enable_reading(self):
        """
        Description: Returns the sensor readings by pass the True flag
        Input Parameters: None
        Output Type: dictionary
        """
        try:
            if self.energymeter_configurations is not None:
                self.energymeter_start_flag = FLAG_STATUS_1
                result = self.get_energymeter_reading(self.energymeter_start_flag)
            else:
                result = Matching().error_mapping(INVALID_CONFIGURATIONS)
                Datalogs.get_instance().logging_error((ERROR_CODE_FORMATTER.format(Matching(
                    ).error_mapping(INVALID_CONFIGURATIONS), ERROR_IN_ENABLE_READING)),
                        SENSORSERROR.format(ENERGYMETER, self.deviceid), Log_levels[ERROR],
                        self.deviceid)
            return {ENERGYMETER:result}
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex

    def diasble_reading(self):
        """
        Description: Disables the sensor readings by setting the flag to False
        Input Parameters: None
        Output Type: string
        """
        try:
            self.energymeter_start_flag = FLAG_STATUS_0
            self.get_energymeter_reading(self.energymeter_start_flag)
            Datalogs.get_instance().logging_error(READING_DISABLED,SENSORSERROR.format(
                ENERGYMETER, self.deviceid), Log_levels[INFO], self.deviceid)
            return READING_DISABLED
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex

    def set_energymeter_configurations(self, data):
        """
        Description: Add device to the sensor configurations file
        Input Parameters: configurations to be added
        Output Type: string
        """
        try:
            with open(CONFIGURATIONS_FILE, READ_WRITE_MODE, encoding="utf-8") as file:
                file_data = json.load(file)
                if list((data).keys())[INDEX_POSITION_0] == ENERGYMETER:
                    new_configuration = {SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]: list(
                        data.values())[INDEX_POSITION_0 ][INDEX_POSITION_0],
                                        SENSORGETSTARTADDRESS[INITIAL_INDEX :FINAL_INDEX ]: list(
                                            data.values())[INDEX_POSITION_0 ][INDEX_POSITION_1],
                                        SENSORGETREGISTERCOUNTS[INITIAL_INDEX :FINAL_INDEX ]: list(
                                            data.values())[INDEX_POSITION_0 ][INDEX_POSITION_2]}
                    count = COUNT_0
                    for position in range(len(file_data[SENSORCONFIGURATIONS.format(ENERGYMETER)])):
                        if file_data[SENSORCONFIGURATIONS.format(ENERGYMETER)][position][
                            SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]] == new_configuration[
                                SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]]:
                            count = count+INCREMENT_1
                            result = DEVICE_ALREADY_EXISTS
                    if count == COUNT_0 :
                        file_data[SENSORCONFIGURATIONS.format(
                            ENERGYMETER)].append(new_configuration)
                        unsorted_configuration = [dict(t) for t in {tuple(
                            d.items()) for d in file_data[SENSORCONFIGURATIONS.format(ENERGYMETER
                                                                                      )]}]
                        file_data[SENSORCONFIGURATIONS.format(ENERGYMETER)] = sorted(
                            unsorted_configuration, key=lambda i:
                                i[SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]])
                        file.truncate(POSTION_0)
                        file.seek(POSTION_0)
                        json.dump(file_data, file, indent=INDENT_LEVEL)
                        Datalogs.get_instance().logging_error(CONFIGURATIONS_ADDED_SUCCESSFULLY,
                                    SENSORSERROR.format(ENERGYMETER, self.deviceid),Log_levels[
                                        INFO], self.deviceid)
                    #self.set_slave_id(new_configuration[SensorGetDeviceID
                    # [initial_index:final_index]])
                        result = NEW_CONFIGURATIONS_ADDED_TO_FILE
                else:
                    Datalogs.get_instance().logging_error((ERROR_CODE_FORMATTER.format(
                        INVALID_INFO, ERROR_IN_SET_ENERGYMETER_CONFIGURATIONS)),SENSORSERROR.format(
                            ENERGYMETER, self.deviceid), Log_levels[ERROR],
                        self.deviceid)
                    result = Matching().error_mapping(INVALID_INFO)
                return {ENERGYMETER:result}
        except FileNotFoundError as ex:
            print("1000",ex.errno)
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                    SENSORSERROR.format(ENERGYMETER, self.deviceid),Log_levels[ERROR],self.deviceid)
            return ex
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex

    def energymeter_reinitiliaze(self):
        """
        Description: Reinitiazes the sensor
        Input Parameters: None
        Output Type: string
        """
        try:
            self.diasble_reading()
            self.energymeter_configurations = None
        except ValueError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[VALUEERROR]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                Log_levels[ERROR], self.deviceid)
            return ex

    def remove_energymeter_configurations(self):
        """
        Description: Removes the configurations the sensor configurations file
        Input Parameters: None
        Output Type: string
        """
        try:
            check_con = COUNT_0
            with open(CONFIGURATIONS_FILE, READ_WRITE_MODE, encoding="utf-8") as file:
                file_data_change = json.load(file)
                file_data = copy.deepcopy(file_data_change)
                energymeter_data = file_data_change[SENSORCONFIGURATIONS.format(ENERGYMETER)]
                for index, _ in enumerate(len(energymeter_data)):
                    if energymeter_data[index][SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]
                                       ] == self.deviceid:
                        check_con = check_con + INCREMENT_1
                        self.energymeter_reinitiliaze()
                        del energymeter_data[index]
                        result = CONFIGURATIONS_REMOVED_SUCCESSFULLY
                if check_con == COUNT_0 :
                    Datalogs.get_instance().logging_error(ENERGYMETER_SENSOR_NOT_FOUND.format(
                        self.deviceid), SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                        Log_levels[ERROR], self.deviceid)
                    result = ENERGYMETER_SENSOR_NOT_FOUND.format(self.deviceid)
                file_data[SENSORCONFIGURATIONS.format(ENERGYMETER)] = energymeter_data
                file.truncate(POSTION_0)
                file.seek(POSTION_0)
                json.dump(file_data, file, indent = INDENT_LEVEL)
            return result
        except FileNotFoundError as ex:
            print("156565",ex.errno)
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(ENERGYMETER, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex
