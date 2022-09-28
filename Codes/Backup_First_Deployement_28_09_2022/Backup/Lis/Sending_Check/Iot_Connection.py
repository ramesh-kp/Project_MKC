from azure.iot.device import IoTHubDeviceClient, Message
from Configurations import Iot_Connection_String


def Iothub_Client_Init():
    iothub_client = IoTHubDeviceClient.create_from_connection_string(
        Iot_Connection_String)
    return iothub_client


def Iothub_Client_Telemetry_Sample_Run(reading):
    try:
        iothub_client = Iothub_Client_Init()
        message = Message(reading)
        print("Sending message: {}".format(message))
        iothub_client.send_message(message)
        print("Message successfully sent")
        # iothub_client.shutdown()

    except Exception as e:
        print(e)
