import copy
import fnmatch
import json
import os
import pathlib
from azure.iot.device import Message
from azure.iot.device.exceptions import CredentialError, ConnectionFailedError, ConnectionDroppedError, ClientError
from azure.iot.device.exceptions import OperationTimeout, NoConnectionError
from File_Management.sensor_data_logging import DeviceDataLogging
from Utilities.util_conversion import FormatMessage
from Utilities.util_error_mapping import Matching

from general_configurations import BASE_DIR, CLIENT_NOT_CONNECTED, CONNECTION_LOST, CONNECTION_TIME_OUT, DIR_PATH, FAILURE_IN_CONNECTION, FILE_NOT_FOUND, INVALID_CREDENTIALS, MKC_WIRAS_SENSOR_DATA, Debug, Error, Error_Code_Formatter, Sensor_readings_send_to_Iot
from general_configurations import Error_in_iothub_client_send_message, Iot, Log_levels
from general_configurations import Message_successfully_sent, Send_Message, SensorDataLogging, SensorsError
from general_configurations import Variable_Header_Sensor_Data, read_write_mode, read_mode, filepath, final_index
from general_configurations import indent_level, postion_0, initial_key_index, final_key_index, increment_1
from general_configurations import min_file_size, min_no_file
from logging_info import Datalogs

class Iotconnection(object):

    def iothub_client_send_message(self, iothub_client, reading):
        """
        Description: To send the relevant information to IotHub.
        Input Parameters: Message needs to sent to IotHub.
        Output Type: None
        """
        try:
            message = Message(str(reading))
            print(Send_Message.format(message))
            iothub_client.send_message(message)
            print(Message_successfully_sent)
        except (CredentialError, ConnectionFailedError, ConnectionDroppedError, OperationTimeout,
                NoConnectionError) as ex:
            Datalogs.getInstance().logging_error((Error_Code_Formatter.format(ex, Error_in_iothub_client_send_message)),
                                                 SensorsError.format(Iot),Log_levels[Error])
            return (Error_Code_Formatter.format(ex, Error_in_iothub_client_send_message))
        except Exception as ex:
            Datalogs.getInstance().logging_error(ex, SensorsError.format(Iot), Log_levels[Debug])
            return ex

    def send_sensor_readings(self, client_obj):
        """
        Description: Open the first file generated,once the sensor readings are send to azure the file is truncated.
        Input parameters: None
        Output type: None
        """
        try:
            list_of_files = os.listdir(DIR_PATH)
            for _ in range(len(list_of_files)):
                first_file = DeviceDataLogging().file_created(0, SensorDataLogging[:final_index])
                path = os.path.join(DIR_PATH,first_file)
                with open(SensorDataLogging.format(first_file), read_write_mode) as file:
                    file_data = json.load(file)
                    final_data = FormatMessage().mqtt_message_format(
                        file_data, Variable_Header_Sensor_Data)
                    result_data = self.iothub_client_send_message(
                        client_obj, final_data)
                    if result_data == None or not result_data:
                        first_key = int(list(file_data.keys())[initial_key_index])
                        last_key = int(list(file_data.keys())[final_key_index])
                        for position in range(first_key, last_key+increment_1):
                            file_data.pop(str(position))
                            file.truncate(postion_0)
                            file.seek(postion_0)
                        json.dump(file_data, file, indent = indent_level)
                        if os.path.getsize(path) <= min_file_size and len([f_name for f_name in os.listdir(DIR_PATH)
                                        if os.path.isfile(os.path.join(DIR_PATH, f_name))]) > min_no_file:
                            os.remove(path)
            return Sensor_readings_send_to_Iot
        except FileNotFoundError as ex:
            Datalogs.getInstance().logging_error(Matching().error_mapping(FILE_NOT_FOUND), SensorsError.format(Iot),
                                                Log_levels[Debug])
            return Matching().error_mapping(FILE_NOT_FOUND)

