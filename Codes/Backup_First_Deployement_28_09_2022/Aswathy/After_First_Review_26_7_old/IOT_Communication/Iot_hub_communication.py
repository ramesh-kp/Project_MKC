import copy
import fnmatch
import json
import os
import pathlib
from azure.iot.device import Message
from File_Management.sensor_data_logging import DeviceDataLogging
from Utilities.util_conversion import FormatMessage

from general_configurations import BASE_DIR, DIR_PATH, MKC_WIRAS_SENSOR_DATA, Message_successfully_sent, Send_Message, SensorDataLogging, Variable_Header_Sensor_Data


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
        except Exception as ex:
            print(ex)

    def send_sensor_readings(self, client_obj):
        """
        Description: Open the first file generated,once the sensor readings are send to azure the file is truncated.
        Input parameters: None
        Output type: None
        """
        list_of_files = os.listdir(DIR_PATH)
        for _ in range(len(list_of_files)):
            first_file = DeviceDataLogging().file_created(0, SensorDataLogging[:-3])
            path = os.path.join(DIR_PATH,first_file)
            with open(SensorDataLogging.format(first_file), 'r+') as file:
                file_data = json.load(file)
                final_data = FormatMessage().mqtt_message_format(
                    file_data, Variable_Header_Sensor_Data)
                result_data = self.iothub_client_send_message(
                    client_obj, final_data)
                if result_data == None or not result_data:
                    first_key = int(list(file_data.keys())[0])
                    last_key = int(list(file_data.keys())[-1])
                    for i in range(first_key, last_key+1):
                        file_data.pop(str(i))
                        file.truncate(0)
                        file.seek(0)
                    json.dump(file_data, file, indent=4)
                    if os.path.getsize(path) <=2 and len([name for name in os.listdir(DIR_PATH)
                                    if os.path.isfile(os.path.join(DIR_PATH, name))]) >1:
                        os.remove(path)

