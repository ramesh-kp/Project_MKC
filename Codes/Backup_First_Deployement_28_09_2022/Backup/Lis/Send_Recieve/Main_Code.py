from Send_Data import Iothub_Client_Telemetry_Sample_Run
from Configurations import send_data
if __name__ == '__main__':
    print(send_data)
    print("Sending Data")
    print("Press Ctrl + C to exit")
    Iothub_Client_Telemetry_Sample_Run(send_data)