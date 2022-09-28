from Azure_Communication import Send_Sensor_Datas
import time

if __name__ == '__main__':
    print("<<< Waste Water Management >>>")
    while True:
        Send_Sensor_Datas.Read_Sensor_Datas().Full_Sensor_Readings()
        time.sleep(2)
