from Azure_Communication import Send_Sensor_Datas
from Azure_Communication import Receive_Azure_Data
from azure.iot.device import IoTHubDeviceClient
from General_Configurations import Sending_Iot_Connection_String
from threading import Event
import threading
from Reception import main


def final_data_config():
    iothub_client = IoTHubDeviceClient.create_from_connection_string(
        Sending_Iot_Connection_String)
    while True:
        Send_Sensor_Datas.Read_Sensor_Datas().send_full_sensor_readings(iothub_client)
        Receive_Azure_Data.azure_data_config(iothub_client)

        Event().wait(3)


if __name__ == '__main__':
    t1 = threading.Thread(target=final_data_config)
    t1.start()
    t2 = threading.Thread(target=main)
    t2.start()
    t2.join()
