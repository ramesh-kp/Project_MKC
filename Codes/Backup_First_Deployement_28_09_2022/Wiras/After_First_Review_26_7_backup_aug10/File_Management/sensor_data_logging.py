"""
This file consist of functions which manages the file operations.
"""
import json
import os
from general_configurations import (
    BASE_DIR,
    MKC2,
    MKC4,
    ValidationError)

class DeviceDataLogging(object):
    """
    This class consist of functions to create json files for writing the sensor readings.
    """

    @classmethod
    def file_created(cls, files_pos):
        """
        Description: Return the Json file which generated.
        Input parameters: file position number
        Output type: Json file
        """
        try:
            reading_dir = os.path.join(BASE_DIR, "Sensor_Data_Logging")
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

    def sensor_readings_log(self, data):
        """
        Description: Open the last file generated,add sensor readings to that file.Once the file reaches 2000 lines,a
        new file is created.
        Input parameters: Sensor readings
        Output type: None
        """
        try:
            latest_file = self.file_created(-1)
            with open(r"Sensor_Data_Logging/{}".format(latest_file), "r+") as file:
                file_data = json.load(file)
                if file_data:
                    last_number = int(list(file_data.keys())[-1])
                    data = {last_number + 1: data}
                else:
                    last_number = 0
                    data = {last_number + 1: data}
                if last_number == 2000:
                    last_number = 1
                file_data.update(data)
                if len(file_data.keys()) <= 2000:
                    file.truncate(0)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                else:
                    file_number = int(latest_file.split("_")[-1].split(".")[0])
                    with open(r"Sensor_Readings/Sensor_Readings_{}.json".format(file_number + 1), "w") as file:
                        file.seek(0)
                        json.dump(data, file, indent=4)
                return True
        except FileNotFoundError:
            return ValidationError[MKC2]
        except Exception:
            return ValidationError[MKC4]


