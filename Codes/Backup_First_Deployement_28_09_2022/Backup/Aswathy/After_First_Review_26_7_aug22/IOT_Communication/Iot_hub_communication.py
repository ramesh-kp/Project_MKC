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

from general_configurations import BASE_DIR, DIR_PATH, MKC2, MKC_WIRAS_SENSOR_DATA, Debug, Error, Error_Code_Formatter
from general_configurations import Error_in_iothub_client_send_message, Iot, Log_levels, ValidationError
from general_configurations import Message_successfully_sent, Send_Message, SensorDataLogging, SensorsError
from general_configurations import Variable_Header_Sensor_Data, read_write_mode, read_mode, filepath, final_index, indent_level
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
        except CredentialError:
            with open(filepath, read_mode) as file:
                error_message = json.load(file)
                Datalogs.getInstance().logging_error((Error_Code_Formatter.format(
                        114, error_message["114"], Error_in_iothub_client_send_message)),SensorsError.format(Iot),
                                                             Log_levels[Warning])
        except ConnectionFailedError:
            with open(filepath, read_mode) as file:
                error_message = json.load(file)
                Datalogs.getInstance().logging_error((Error_Code_Formatter.format(
                        115, error_message["115"], Error_in_iothub_client_send_message)),SensorsError.format(Iot),
                                                             Log_levels[Warning])
        except ConnectionDroppedError:
            with open(filepath, read_mode) as file:
                error_message = json.load(file)
                Datalogs.getInstance().logging_error((Error_Code_Formatter.format(
                        116, error_message["116"], Error_in_iothub_client_send_message)),SensorsError.format(Iot),
                                                             Log_levels[Warning])
        except OperationTimeout:
            with open(filepath, read_mode) as file:
                error_message = json.load(file)
                Datalogs.getInstance().logging_error((Error_Code_Formatter.format(
                        117, error_message["117"], Error_in_iothub_client_send_message)),SensorsError.format(Iot),
                                                             Log_levels[Warning])
        except NoConnectionError:
            with open(filepath, read_mode) as file:
                error_message = json.load(file)
                Datalogs.getInstance().logging_error((Error_Code_Formatter.format(
                        118, error_message["118"], Error_in_iothub_client_send_message)),SensorsError.format(Iot),
                                                             Log_levels[Warning])
        except ClientError:
            with open(filepath, read_mode) as file:
                error_message = json.load(file)
                Datalogs.getInstance().logging_error((Error_Code_Formatter.format(
                        119, error_message["119"], Error_in_iothub_client_send_message)),SensorsError.format(Iot),
                                                             Log_levels[Warning])
        except Exception as ex:
            Datalogs.getInstance().logging_error(ex, SensorsError.format(Iot),
                                                         Log_levels[Debug])
            print(ex)

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
                        first_key = int(list(file_data.keys())[0])
                        last_key = int(list(file_data.keys())[-1])
                        for position in range(first_key, last_key+1):
                            file_data.pop(str(position))
                            file.truncate(0)
                            file.seek(0)
                        json.dump(file_data, file, indent = indent_level)
                        if os.path.getsize(path) <=2 and len([f_name for f_name in os.listdir(DIR_PATH)
                                        if os.path.isfile(os.path.join(DIR_PATH, f_name))]) >1:
                            os.remove(path)
        except FileNotFoundError as ex:
            Datalogs.getInstance().logging_error(ValidationError[MKC2], SensorsError.format(Iot),
                                                Log_levels[Debug])
            return ValidationError[MKC2]
        except Exception as ex:
            return ex

