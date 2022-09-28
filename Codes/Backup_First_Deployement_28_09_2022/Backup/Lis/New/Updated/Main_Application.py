from multiprocessing import Semaphore
from Azure_Communication import Send_Sensor_Datas
from Azure_Communication import Receive_Azure_Data
import time
if __name__ == '__main__':
    print("<<< Waste Water Management >>>")
    obj = Semaphore()
    obj.acquire()
    while True:
        # frequency_time = float(Send_Sensor_Datas().Read_Frequency())
        # Receive_Azure_Data.Azure_data_Config()
        # obj.acquire()
        Send_Sensor_Datas.Read_Sensor_Datas().Full_Sensor_Readings()
        obj.release()
        
