import asyncio
from Azure_Communication import Send_Sensor_Datas
from Azure_Communication import Receive_Azure_Data
import time
# import _asyncio
from threading import Event
if __name__ == '__main__':
    print("<<< Waste Water Management >>>")
    # while True:
    #     # frequency_time = float(Send_Sensor_Datas().Read_Frequency())
    #     # Receive_Azure_Data.Azure_data_Config()
    #     Send_Sensor_Datas.Read_Sensor_Datas().Full_Sensor_Readings()
    #     time.sleep(3)

    # while True:
    #     async def display():
    #         await asyncio.sleep(2)
    #         Send_Sensor_Datas.Read_Sensor_Datas().Full_Sensor_Readings()
    #     asyncio.run(display())

    while True:
        def display():
            Send_Sensor_Datas.Read_Sensor_Datas().Full_Sensor_Readings()

        Event().wait(3)
        display()
