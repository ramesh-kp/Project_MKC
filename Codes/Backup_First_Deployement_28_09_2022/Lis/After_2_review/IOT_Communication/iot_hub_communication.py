"""
# This file consist of functions that send readingsand other messages to IOT
"""
import json
import os

from azure.iot.device import Message
from azure.iot.device.exceptions import CredentialError, ConnectionFailedError
from azure.iot.device.exceptions import OperationTimeout, NoConnectionError,ConnectionDroppedError
from logging_info import Datalogs
from File_Management.sensor_data_logging import DeviceDataLogging
from Utilities.util_conversion import FormatMessage
from Utilities.util_error_mapping import Matching

# from general_configurations import BASE_DIR, CLIENT_NOT_CONNECTED, CONNECTION_LOST
from general_configurations import DIR_PATH, FILE_NOT_FOUND
from general_configurations import  DEBUG, ERROR
from general_configurations import ERROR_CODE_FORMATTER, SENSOR_READINGS_SEND_TO_IOT
from general_configurations import SENSORSERROR, FINAL_INDEX, INCREMENT_1
from general_configurations import ERROR_IN_IOTHUB_CLIENT_SEND_MESSAGE, IOT, Log_levels
from general_configurations import MESSAGE_SUCCESSFULLY_SENT, SEND_MESSAGE, SENSORDATALOGGING
from general_configurations import Variable_Header_Sensor_Data, READ_WRITE_MODE
from general_configurations import INDENT_LEVEL, POSTION_0 , INITIAL_KEY_INDEX , FINAL_KEY_INDEX
from general_configurations import MIN_FILE_SIZE , MIN_NO_FILE


class Iotconnection(object):
    """
    This class consist of functions that send readingsand other messages to IOT
    """

    def iothub_client_send_message(self, iothub_client, reading):
        """
        Description: To send the relevant information to IotHub.
        Input Parameters: Message needs to sent to IotHub.
        Output Type: None
        """
        try:
            message = Message(str(reading))
            print(SEND_MESSAGE.format(message))
            iothub_client.send_message(message)
            print(MESSAGE_SUCCESSFULLY_SENT)
        except (CredentialError, ConnectionFailedError, ConnectionDroppedError, OperationTimeout,
                NoConnectionError) as ex:
            Datalogs.getInstance().logging_error((ERROR_CODE_FORMATTER.format(ex,
                    ERROR_IN_IOTHUB_CLIENT_SEND_MESSAGE)),
                                                 SENSORSERROR.format(IOT),Log_levels[ERROR])
            return ERROR_CODE_FORMATTER.format(ex, ERROR_IN_IOTHUB_CLIENT_SEND_MESSAGE)

    def send_sensor_readings(self, client_obj):
        """
        Description: Open the first file generated,once the sensor readings are send to azure the file is truncated.
        Input parameters: client_obj
        Output type: String
        """
        try:
            list_of_files = os.listdir(DIR_PATH)
            for _ in range(len(list_of_files)):
                first_file = DeviceDataLogging().file_created(0, SENSORDATALOGGING[:FINAL_INDEX ])
                path = os.path.join(DIR_PATH,first_file)
                with open(SENSORDATALOGGING.format(first_file), READ_WRITE_MODE,
                          encoding="utf-8") as file:
                    file_data = json.load(file)
                    final_data = FormatMessage().mqtt_message_format(
                        file_data, Variable_Header_Sensor_Data)
                    result_data = self.iothub_client_send_message(
                        client_obj, final_data)
                    if result_data is None or not result_data:
                        first_key = int(list(file_data.keys())[INITIAL_KEY_INDEX ])
                        last_key = int(list(file_data.keys())[FINAL_KEY_INDEX ])
                        for position in range(first_key, last_key+INCREMENT_1):
                            file_data.pop(str(position))
                            file.truncate(POSTION_0 )
                            file.seek(POSTION_0 )
                        json.dump(file_data, file, indent = INDENT_LEVEL)
                        if os.path.getsize(path) <= MIN_FILE_SIZE  and len([f_name for f_name in
                                os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH,
                                f_name))]) > MIN_NO_FILE:
                            os.remove(path)
            return SENSOR_READINGS_SEND_TO_IOT
        except FileNotFoundError:
            Datalogs.getInstance().logging_error(Matching().error_mapping(FILE_NOT_FOUND),
                                                 SENSORSERROR.format(IOT),Log_levels[DEBUG])
            return Matching().error_mapping(FILE_NOT_FOUND)
