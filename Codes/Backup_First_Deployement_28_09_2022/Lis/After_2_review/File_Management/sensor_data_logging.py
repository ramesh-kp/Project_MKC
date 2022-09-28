"""
This file consist of functions which manages the file operations.
"""
import json
import os
from logging_info import Datalogs

from Utilities.util_error_mapping import Matching
from general_configurations import (
    BASE_DIR,
    FILE_NOT_FOUND,
    LIST_INDEX_ERROR,
    DEBUG,
    ERROR,
    FUNCTION ,
    INFO ,
    Log_levels,
    READINGS_WRITTEN_TO_FILE,
    SENSORDATALOGGING,
    SENSORREADINGSCREATENEWFILE,
    SENSOREADINGSEXTERNAL,
    SENSORSERROR,
    WRITE_MODE,
    READ_WRITE_MODE,
    LAST_POSITION ,
    LINE_NUMBER_0  ,
    LINE_NUMBER_300,
    LINE_NUMBER_1,
    FINAL_INDEX ,
    DOT ,
    UNDERSCORE ,
    INDENT_LEVEL)




class DeviceDataLogging(object):
    """
    This class consist of functions to create json files for writing the sensor readings.
    """

    @classmethod
    def file_created(cls, files_pos, folder_name):
        """
        Description: Return the Json file which generated.
        Input parameters: file position number and folder name
        Output type: Json file
        """
        try:
            reading_dir = os.path.join(BASE_DIR, folder_name)
            list_of_files = list(
                filter(
                    lambda x: os.path.isfile(os.path.join(reading_dir, x)),
                    os.listdir(reading_dir),
                )
            )
            list_of_files = sorted(
                list_of_files,
                key=lambda x: os.path.getmtime(os.path.join(reading_dir, x)),
            )
            return str(list_of_files[files_pos])
        except FileNotFoundError:
            Datalogs.getInstance().logging_error(Matching().error_mapping(FILE_NOT_FOUND),
                        SENSORSERROR.format(FUNCTION), Log_levels[DEBUG])
            return Matching().error_mapping(FILE_NOT_FOUND)
        except IndexError:
            Datalogs.getInstance().logging_error(Matching().error_mapping(LIST_INDEX_ERROR),
                        SENSORSERROR.format(FUNCTION ),Log_levels[DEBUG])
            return Matching().error_mapping(LIST_INDEX_ERROR)

    @classmethod
    def file_operation(cls, file_name, data, latest_file, file_path):
        """
        Description: Return the Json file which generated.
        Input parameters: file position number and folder name
        Output type: Json file
        """
        try:
            file_data = json.load(file_name)
            if file_data:
                last_number = int(list(file_data.keys())[LAST_POSITION ])
            else:
                last_number = LINE_NUMBER_0
            data = {last_number + 1: data}
            if last_number == LINE_NUMBER_300:
                last_number = LINE_NUMBER_1
            file_data.update(data)
            if len(file_data.keys()) <= LINE_NUMBER_300:
                file_name.truncate(0)
                file_name.seek(0)
                json.dump(file_data, file_name, indent = INDENT_LEVEL)
            else:
                new_data = list(data.values())[0]
                last_number = 0
                data = {last_number + 1: new_data}
                file_number = int(latest_file.split(UNDERSCORE )[LAST_POSITION ].split(DOT )[0])
                with open(SENSORREADINGSCREATENEWFILE.format(file_path, (file_number + 1)),
                          WRITE_MODE, encoding="utf-8") as file:
                    file.seek(0)
                    json.dump(data, file, indent=INDENT_LEVEL)
        except FileNotFoundError as ex:
            Datalogs.getInstance().logging_error(ex, SENSORSERROR.format(FUNCTION ),
                                                Log_levels[ERROR])
            return ex

    def set_mode(self,flag):
        """
        Description: Return the boolean flag.
        Input parameters: True or False
        Output type: Boolean
        """
        if flag is False:
            return flag
        if flag is  True:
            return flag

    def sensor_readings_log(self, data, flag):
        """
        Description: Open the last file generated,add sensor readings to that file.Once th0
        file reaches 2000 lines,a new file is created.
        Input parameters: Sensor readings, flag
        Output type: None
        """
        try:
            if flag is False:
                latest_file = self.file_created(-1, SENSORDATALOGGING[:FINAL_INDEX ])
                with open(SENSORDATALOGGING.format(latest_file), READ_WRITE_MODE,
                          encoding="utf-8") as internal_file:
                    self.file_operation(internal_file, data,
                                        latest_file, SENSORDATALOGGING[:FINAL_INDEX ])
            else:
                latest_file = self.file_created(-1, SENSOREADINGSEXTERNAL[:FINAL_INDEX ])
                with open(SENSOREADINGSEXTERNAL.format(latest_file), READ_WRITE_MODE,
                          encoding="utf-8") as external_file:
                    self.file_operation(external_file, data,
                                        latest_file, SENSOREADINGSEXTERNAL[:FINAL_INDEX ])
            Datalogs.getInstance().logging_error(READINGS_WRITTEN_TO_FILE,
                                SENSORSERROR.format(FUNCTION ), Log_levels[INFO ])
            return True
        except FileNotFoundError:
            Datalogs.getInstance().logging_error(Matching().error_mapping(FILE_NOT_FOUND),
                            SENSORSERROR.format(FUNCTION ),Log_levels[DEBUG])
            return Matching().error_mapping(FILE_NOT_FOUND)
        except IndexError:
            Datalogs.getInstance().logging_error(Matching().error_mapping(LIST_INDEX_ERROR),
                                SENSORSERROR.format(FUNCTION), Log_levels[DEBUG])
            return Matching().error_mapping(LIST_INDEX_ERROR)

