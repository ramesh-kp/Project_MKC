from azure.iot.device import Message

from general_configurations import MKC_WIRAS_SENSOR_DATA

class Iotconnection(object):

    def iothub_client_send_message(self, iothub_client, reading):
        """
        Description: To send the relevant information to IotHub.
        Input Parameters: Message needs to sent to IotHub.
        Output Type: None
        """
        try:
            message = Message(str(reading))
            print("Sending message: {}".format(message))
            iothub_client.send_message(message)
            print("Message_successfully_sent")
        except Exception as ex:
            print(ex)

    def azure_read(self, client_obj):
        """
        Description: The input message is converted to the data received from the sensors.
        Input Parameters: None
        Output type: Dictionary if message is received appropriately else a string.
        """
        try:
            with open(Azure_Read_Data_File, 'r') as file:
                azure_data = json.load(file)
            for key in azure_data.keys():
                azure_input = azure_data[key]
            with open(Azure_Read_Data_File, 'w') as file:
                json.dump([], file)
            total_length = int(azure_input[2:10], 16)
            variable_length = int(azure_input[10:18], 16)
            topic_name = azure_input[18: 18 + variable_length]
            if topic_name == MKC_WIRAS_SENSOR_DATA:
            # if topic_name == MKC_WIRAS_CONFIGURATION:
                message_length = int(
                    azure_input[18 + variable_length: 26 + variable_length], 16)
                message_content = azure_input[26 + variable_length:]
                message_content_length = len(
                    azure_input[26 + variable_length:])
                if total_length == (variable_length + message_length + 16):
                    if message_content_length == message_length:
                        receive_data = ast.literal_eval(message_content)
                        DataLogs().receive_data_logs(receive_data)
                        receive_data_ack = SendSensorData().mqtt_message_format(
                            receive_data, Variable_Header_Configuration_Ack)
                        SendSensorData().iothub_client_send_message(client_obj,
                                                                    receive_data_ack)
                        self.set_frequency_time(receive_data)
                        self.set_sensor_configuration(receive_data)
                        self.set_clear_configuration(receive_data)

                else:
                    print("The_message_is_not_being_received_appropriately")
            else:
                print("Incorrect_Topic_name")
        except Exception as ex:
            print(ex)