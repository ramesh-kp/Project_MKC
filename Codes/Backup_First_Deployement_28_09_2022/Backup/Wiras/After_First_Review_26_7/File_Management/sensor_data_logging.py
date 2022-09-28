"""
This file consist of functions which manages the file operations.
"""
import json
import os
from general_configurations import (
    BASE_DIR,
    MKC2,
    MKC4,
    Debug,
    Error,
    Function,
    Info,
    Log_levels,
    Readings_written_to_file,
    SensorDataLogging,
    SensorReadingsCreateNewFile,
    SensorReadingsExternal,
    SensorsError,
    ValidationError,
    write_mode,
    read_write_mode,
    last_position,
    line_number_0,
    line_number_300,
    line_number_1,
    final_index,
    dot,
    underscore,
    indent_level)
from logging_info import Datalogs


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
            Datalogs.getInstance().logging_error(ValidationError[MKC2], SensorsError.format(Function),
                                                Log_levels[Debug])
            return ValidationError[MKC2]
        except IndexError:
            Datalogs.getInstance().logging_error(ValidationError[MKC4], SensorsError.format(Function),
                                                Log_levels[Debug])
            return ValidationError[MKC4]

    @classmethod
    def file_operation(cls, file_name, data, latest_file, file_path):
        try:
            file_data = json.load(file_name)
            if file_data:
                last_number = int(list(file_data.keys())[last_position])
            else:
                last_number = line_number_0
            data = {last_number + 1: data}
            if last_number == line_number_300:
                last_number = line_number_1
            file_data.update(data)
            if len(file_data.keys()) <= line_number_300:
                file_name.truncate(0)
                file_name.seek(0)
                json.dump(file_data, file_name, indent = indent_level)
            else:
                new_data = list(data.values())[0]
                last_number = 0
                data = {last_number + 1: new_data}
                file_number = int(latest_file.split(underscore)[last_position].split(dot)[0])
                with open(SensorReadingsCreateNewFile.format(file_path, (file_number + 1)), write_mode) as file:
                    file.seek(0)
                    json.dump(data, file, indent=indent_level)
        except Exception as ex:
            Datalogs.getInstance().logging_error(ex, SensorsError.format(Function),
                                                Log_levels[Error])
            return ex

    def set_mode(self,flag):
        if flag == False:
            return flag
        if flag == True:
            return flag

    def sensor_readings_log(self, data, flag):
        """
        Description: Open the last file generated,add sensor readings to that file.Once the file reaches 2000 lines,a
        new file is created.
        Input parameters: Sensor readings, flag
        Output type: None
        """
        try:
            if flag == False:
                latest_file = self.file_created(-1, SensorDataLogging[:final_index])
                with open(SensorDataLogging.format(latest_file), read_write_mode) as internal_file:
                    self.file_operation(internal_file, data,
                                        latest_file, SensorDataLogging[:final_index])
            else:
                latest_file = self.file_created(-1, SensorReadingsExternal[:final_index])
                with open(SensorReadingsExternal.format(latest_file), read_write_mode) as external_file:
                    self.file_operation(external_file, data,
                                        latest_file, SensorReadingsExternal[:final_index])
            Datalogs.getInstance().logging_error(Readings_written_to_file, SensorsError.format(Function),
                                                Log_levels[Info])
            return True
        except FileNotFoundError:
            Datalogs.getInstance().logging_error(ValidationError[MKC2], SensorsError.format(Function),
                                                Log_levels[Debug])
            return ValidationError[MKC2]
        except IndexError:
            Datalogs.getInstance().logging_error(ValidationError[MKC4], SensorsError.format(Function),
                                                Log_levels[Debug])
            return ValidationError[MKC4]
        except Exception as ex:
            Datalogs.getInstance().logging_error(ex, SensorsError.format(Function),
                                                Log_levels[Error])
            return ex
