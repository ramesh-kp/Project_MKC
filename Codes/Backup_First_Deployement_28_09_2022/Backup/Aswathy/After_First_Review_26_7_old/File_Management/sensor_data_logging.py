"""
This file consist of functions which manages the file operations.
"""
import json
import os
from general_configurations import (
    BASE_DIR,
    MKC2,
    MKC4,
    SensorDataLogging,
    SensorReadingsCreateNewFile,
    SensorReadingsExternal,
    ValidationError)


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
            return ValidationError[MKC2]

    @classmethod
    def file_operation(cls, file_name, data, latest_file, file_path):
        file_data = json.load(file_name)
        if file_data:
            last_number = int(list(file_data.keys())[-1])
        else:
            last_number = 0
        data = {last_number + 1: data}
        if last_number == 300:
            last_number = 1
        file_data.update(data)
        if len(file_data.keys()) <= 300:
            file_name.truncate(0)
            file_name.seek(0)
            json.dump(file_data, file_name, indent=4)
        else:
            new_data = list(data.values())[0]
            last_number = 0
            data = {last_number + 1: new_data}
            file_number = int(latest_file.split("_")[-1].split(".")[0])
            with open(SensorReadingsCreateNewFile.format(file_path, (file_number + 1)), "w") as file:
                file.seek(0)
                json.dump(data, file, indent=4)

    def set_mode(self,flag):
        if flag == False:
            return flag
        if flag == True:
            return flag

    def sensor_readings_log(self, data, flag):
        """
        Description: Open the last file generated,add sensor readings to that file.Once the file reaches 2000 lines,a
        new file is created.
        Input parameters: Sensor readings
        Output type: None
        """
        try:
            if flag == False:
                latest_file = self.file_created(-1, SensorDataLogging[:-3])
                with open(SensorDataLogging.format(latest_file), "r+") as internal_file:
                    self.file_operation(internal_file, data,
                                        latest_file, SensorDataLogging[:-3])
            else:
                latest_file = self.file_created(-1, SensorReadingsExternal[:-3])
                with open(SensorReadingsExternal.format(latest_file), "r+") as external_file:
                    self.file_operation(external_file, data,
                                        latest_file, SensorReadingsExternal[:-3])
            return True
        except FileNotFoundError:
            return ValidationError[MKC2]
        except Exception:
            return ValidationError[MKC4]
