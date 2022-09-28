"""
This document demonstrates function in relation with PH Sensor
"""
import copy
import json

from Utilities.util_device_communication import DeviceCommunication
from Utilities.util_conversion import Conversion
from Utilities.util_error_mapping import Matching

from general_configurations import ATTRIBUTEERROR, CONNECTIONEXCEPTION, FILENOTFOUND
from general_configurations import CONFIGURATIONS_FILE, READ_MODE
from general_configurations import FLAG_STATUS_0 , PH, INDEXERROR, VALUEERROR, Error_number
from general_configurations import INFO_NOT_FOUND_IN_FILE, INDENT_LEVEL, INCREMENT_1
from general_configurations import ADDED_DEVICE_SUCCESSFULLY, PH_SENSOR_NOT_FOUND
from general_configurations import CONFIGURATIONS_ADDED_SUCCESSFULLY, COUNT_0
from general_configurations import INVALID_CONFIGURATIONS, INVALID_DATA_FROM_MODBUS
from general_configurations import INVALID_INFO, INVALID_SLAVE_ID, ERROR_CODE_FORMATTER
from general_configurations import CONFIGURATIONS_REMOVED_SUCCESSFULLY, DEBUG, ERROR
from general_configurations import ERRORMESSAGESENSOR, Log_levels, UNABLE_TO_ADD_DEVICE
from general_configurations import SENSORGETDEFAULTID, INITIAL_INDEX , INDEX_POSITION_2
from general_configurations import MODBUSCONNECTIONERROR, POSITION_1, POSITION_2
from general_configurations import (
    ERROR_IN_ENABLE_READING,
    ERROR_IN_SET_PH_CONFIGURATIONS,
)
from general_configurations import (
    INFO,
    NEW_CONFIGURATIONS_ADDED_TO_FILE
)
from general_configurations import MODBUSERRORMESSAGE, MODBUSSLAVEIDERRORMESSAGE
from general_configurations import (
    RECEIVED_READINGS_FROM_SENSOR,
    SENSORGETDATA,
    SENSORGETDEVICEID,
)
from general_configurations import (
    SENSORSERROR,
    SENSORCONFIGURATIONS,
    SENSORGETSTARTADDRESS,
)
from general_configurations import SENSORGETREGISTERCOUNTS, DEVICE_ALREADY_EXISTS
from general_configurations import (
    SENSOR_ADDRESS_FILE,
    SENSORGETADDRESS,
    READ_WRITE_MODE,
    READING_DISABLED
)
from general_configurations import ARRAY_POSITION_0 , ARRAY_POSITION_1 , ARRAY_POSITION_2
from general_configurations import FINAL_INDEX , INDEX_POSITION_0 , INDEX_POSITION_1
from general_configurations import (
    POSTION_0,
    FLAG_STATUS_1,
    CONNECTION_COUNT_0,
    CONNECTION_COUNT_10,
    PH_ARRAY_POS_1,
    PH_ARRAY_POS_2
)

from logging_info import Datalogs

class PhSensor(object):
    """
    This class contain functions which initilize configurations of Ph and its array position
    for getting the Ph data from the Ph reading.It contain functions which reads the data from
    Ph Sensor.
    """
    modbuserror = MODBUSERRORMESSAGE
    modbusslaveiderror = MODBUSSLAVEIDERRORMESSAGE

    def __init__(self,deviceid = None):
        self.deviceid = deviceid
        self.ph_start_flag = FLAG_STATUS_0
        self.ph_configurations = None
        self.ph_data_position = [PH_ARRAY_POS_1 , PH_ARRAY_POS_2 ]
        self.ph_configurations = self.get_ph_configurations()
    def get_ph_configurations(self):
        """
        Description: Returns the ph configurations from Sensor_Configuration_File.
        Input Parameters: None
        Output Type: list
        """

        try:
            config_list = []
            with open(CONFIGURATIONS_FILE, READ_MODE, encoding="utf-8") as file:
                file_data = json.load(file)
                if file_data and SENSORCONFIGURATIONS.format(PH) in file_data:
                    for position in range(len(file_data[SENSORCONFIGURATIONS.format(PH)])):
                        config_list.append(
                            list(file_data[SENSORCONFIGURATIONS.format(PH)][position].values()))
                    self.ph_configurations = config_list
                    result =  config_list
                else:
                    result =  None
                    Datalogs().logging_error(Matching().error_mapping(INFO_NOT_FOUND_IN_FILE),
                            SENSORSERROR.format(PH, self.deviceid), Log_levels[DEBUG],self.deviceid)
                return result
        except FileNotFoundError as ex:
            Datalogs.get_instance().logging_error((ex, Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex
        except AttributeError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[ATTRIBUTEERROR]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
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
                sensor_result.update({SENSORGETDEVICEID.format(PH, position):
                    self.ph_configurations[position][ARRAY_POSITION_0 ],
                    ERRORMESSAGESENSOR.format(PH, position): result})
            else:
                sensor_result.update({SENSORGETDEVICEID.format(PH, position):
                    self.ph_configurations[position][ARRAY_POSITION_0 ],
                    SENSORGETDATA.format(PH, position): Conversion().parse_rawdata(
                        sensor_reading.registers,self.ph_data_position[POSITION_1],
                        self.ph_data_position[POSITION_2])})
            return sensor_result
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex, Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(PH,self.deviceid),
                                                Log_levels[ERROR], self.deviceid)
            return ex


    def get_ph_reading(self, ph_start_flag):
        """
        Description: Returns the final output from the sensor readings
        Input Parameters: ph_start_flag which is either True or False
        Output Type: dictionary
        """
        try:
            ph_data = {}
            for position, _ in enumerate(self.ph_configurations):
                while True:
                    if (ph_start_flag == FLAG_STATUS_1) and (self.deviceid ==
                                self.ph_configurations[position][ARRAY_POSITION_0 ]):
                        ph_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                            count = self.ph_configurations[position][ARRAY_POSITION_2],
                            address=self.ph_configurations[position][ARRAY_POSITION_1 ],
                            unit=self.ph_configurations[position][ARRAY_POSITION_0]))
                        ph_data.update(self.validate_content(ph_reading, position))
                        Datalogs.get_instance().logging_error(RECEIVED_READINGS_FROM_SENSOR,
                                    SENSORSERROR.format(PH, self.deviceid), Log_levels[INFO],
                                    self.deviceid)
                        if None not in ph_data.values():
                            break
                    else:
                        break
            return ph_data
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex, Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return {ERRORMESSAGESENSOR.format(PH, self.deviceid):ex}
        except Exception as ex:
            if type(ex).__name__ == CONNECTIONEXCEPTION:
                result = {ERRORMESSAGESENSOR.format(PH, self.deviceid):MODBUSCONNECTIONERROR}
            else:
                result = {ERRORMESSAGESENSOR.format(PH, self.deviceid):ex}
            Datalogs.get_instance().logging_error(ex,
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return result

    def enable_reading(self):
        """
        Description: Returns the sensor readings by pass the True flag
        Input Parameters: None
        Output Type: dictionary
        """
        try:
            if self.ph_configurations is not None:
                self.ph_start_flag = FLAG_STATUS_1
                result = self.get_ph_reading(self.ph_start_flag)
            else:
                result = Matching().error_mapping(INVALID_CONFIGURATIONS)
                Datalogs.get_instance().logging_error((ERROR_CODE_FORMATTER.format(Matching(
                    ).error_mapping(INVALID_CONFIGURATIONS), ERROR_IN_ENABLE_READING)),
                        SENSORSERROR.format(PH, self.deviceid), Log_levels[ERROR], self.deviceid)
            return {PH:result}
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex

    def diasble_reading(self):
        """
        Description: Disables the sensor readings by setting the flag to False
        Input Parameters: None
        Output Type: string
        """
        try:
            self.ph_start_flag = FLAG_STATUS_0
            self.get_ph_reading(self.ph_start_flag)
            Datalogs.get_instance().logging_error(READING_DISABLED,SENSORSERROR.format(
                PH, self.deviceid), Log_levels[INFO], self.deviceid)
            return READING_DISABLED
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[INDEXERROR]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex

    def add_device(self, new_slave_id):
        """
        Description: set new device id to the sensors
        Input Parameters: new_slave_id
        Output Type: string
        """
        try:
            res = None
            count = 0
            while count < 3:
                with open(SENSOR_ADDRESS_FILE, READ_MODE, encoding="utf-8") as file:
                    data = json.load(file)
                    sensor_address = data[SENSORGETADDRESS[INITIAL_INDEX :FINAL_INDEX ]
                                        ][SENSORGETSTARTADDRESS[:FINAL_INDEX ].format(PH)]
                    sensor_id = data[SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]
                                    ][SENSORGETDEFAULTID[:FINAL_INDEX ].format(PH)]
                    res = DeviceCommunication().gateway_connect().write_registers(
                        address=sensor_address,
                        values=Conversion().little_to_big_endian(new_slave_id),
                        unit=int(sensor_id))
                    if res is None:
                        count = count+1
                    else:
                        result = ADDED_DEVICE_SUCCESSFULLY
                        break
                    # address - Starting Address
                    # values - Values to write
                    # unit - Current Slave Id
                    print(res)
                    Datalogs.get_instance().logging_error(ADDED_DEVICE_SUCCESSFULLY,
                                    SENSORSERROR.format(PH), Log_levels[INFO], self.deviceid)
                    result = ADDED_DEVICE_SUCCESSFULLY
            if count >= 3:
                result = UNABLE_TO_ADD_DEVICE
            return {PH:result}
        except FileNotFoundError as ex:
            print("999",ex.errno)
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(PH),
                                                  Log_levels[DEBUG], self.deviceid)
            return ex


    def set_ph_configurations(self, data):
        """
        Description: Add device to the sensor configurations file
        Input Parameters: configurations to be added
        Output Type: string
        """
        try:
            with open(CONFIGURATIONS_FILE, READ_WRITE_MODE, encoding="utf-8") as file:
                file_data = json.load(file)
                if list((data).keys())[INDEX_POSITION_0 ] == PH:
                    new_configuration = {SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]: list(
                        data.values())[INDEX_POSITION_0 ][INDEX_POSITION_0 ],
                                        SENSORGETSTARTADDRESS[INITIAL_INDEX :FINAL_INDEX ]: list(
                                            data.values())[INDEX_POSITION_0 ][INDEX_POSITION_1],
                                        SENSORGETREGISTERCOUNTS[INITIAL_INDEX :FINAL_INDEX ]: list(
                                            data.values())[INDEX_POSITION_0 ][INDEX_POSITION_2]}
                    count = COUNT_0
                    for position in range(len(file_data[SENSORCONFIGURATIONS.format(PH)])):
                        if file_data[SENSORCONFIGURATIONS.format(PH)][position][SENSORGETDEVICEID[
                            INITIAL_INDEX :FINAL_INDEX ]] == new_configuration[SENSORGETDEVICEID
                                                            [INITIAL_INDEX :FINAL_INDEX ]]:
                            count = count+INCREMENT_1
                            result = DEVICE_ALREADY_EXISTS
                    if count == COUNT_0 :
                        file_data[SENSORCONFIGURATIONS.format(
                            PH)].append(new_configuration)
                        unsorted_configuration = [dict(t) for t in {tuple(
                            d.items()) for d in file_data[SENSORCONFIGURATIONS.format(PH)]}]
                        file_data[SENSORCONFIGURATIONS.format(PH)] = sorted(
                            unsorted_configuration, key=lambda i:
                                i[SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]])
                        file.truncate(POSTION_0)
                        file.seek(POSTION_0)
                        json.dump(file_data, file, indent=INDENT_LEVEL)
                        Datalogs.get_instance().logging_error(CONFIGURATIONS_ADDED_SUCCESSFULLY,
                                    SENSORSERROR.format(PH, self.deviceid),Log_levels[INFO],
                                    self.deviceid)
                    #self.set_slave_id(new_configuration[SensorGetDeviceID
                    # [initial_index:final_index]])
                        result = NEW_CONFIGURATIONS_ADDED_TO_FILE
                else:
                    Datalogs.get_instance().logging_error((ERROR_CODE_FORMATTER.format(
                        INVALID_INFO, ERROR_IN_SET_PH_CONFIGURATIONS)),SENSORSERROR.format(
                            PH, self.deviceid), Log_levels[ERROR],
                        self.deviceid)
                    result = Matching().error_mapping(INVALID_INFO)
                return {PH:result}
        except FileNotFoundError as ex:
            print("1000",ex.errno)
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                    SENSORSERROR.format(PH, self.deviceid),Log_levels[ERROR],self.deviceid)
            return ex
        except IndexError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex

    def ph_reinitiliaze(self):
        """
        Description: Reinitiazes the sensor
        Input Parameters: None
        Output Type: string
        """
        try:
            self.diasble_reading()
            self.ph_configurations = None
        except ValueError as ex:
            Datalogs.get_instance().logging_error((ex,Error_number[VALUEERROR]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                Log_levels[ERROR], self.deviceid)
            return ex

    def remove_ph_configurations(self):
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
                ph_data = file_data_change[SENSORCONFIGURATIONS.format(PH)]
                for index, _ in enumerate(len(ph_data)):
                    if ph_data[index][SENSORGETDEVICEID[INITIAL_INDEX :FINAL_INDEX ]
                                       ] == self.deviceid:
                        check_con = check_con + INCREMENT_1
                        self.ph_reinitiliaze()
                        del ph_data[index]
                        result = CONFIGURATIONS_REMOVED_SUCCESSFULLY
                if check_con == COUNT_0 :
                    Datalogs.get_instance().logging_error(PH_SENSOR_NOT_FOUND.format(
                        self.deviceid), SENSORSERROR.format(PH, self.deviceid),
                                                        Log_levels[ERROR], self.deviceid)
                    result = PH_SENSOR_NOT_FOUND.format(self.deviceid)
                file_data[SENSORCONFIGURATIONS.format(PH)] = ph_data
                file.truncate(POSTION_0)
                file.seek(POSTION_0)
                json.dump(file_data, file, indent = INDENT_LEVEL)
            return result
        except FileNotFoundError as ex:
            print("156565",ex.errno)
            Datalogs.get_instance().logging_error((ex,Error_number[FILENOTFOUND]),
                                                  SENSORSERROR.format(PH, self.deviceid),
                                                  Log_levels[ERROR], self.deviceid)
            return ex
