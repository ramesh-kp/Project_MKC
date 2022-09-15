from pymodbus.client.sync import ModbusTcpClient

Gateway_Ip_Address = "192.168.1.254"
Gateway_Port = "502"

Water_Level_Sensor_Device_Id = 1
Water_Level_Sensor_Start_Address = 8
Water_Level_Sensor_Register_Counts = 2

Ethernet_Network_Error = {"Error_Message": "Error in Ethernet Network"}


def Gateway_Connect():
    gateway_client = ModbusTcpClient(Gateway_Ip_Address, int(Gateway_Port))
    gateway_client.connect()
    # time.sleep(2)
    return gateway_client


def Water_Level_Reading():
    """
    Water Level Reading
    """
    Connection_Checking_Count = 0
    try:
        while True:
            print("Water Level")
            Water_Level_Reading = Gateway_Connect().read_input_registers(count=int(Water_Level_Sensor_Register_Counts),
                                                                         address=int(Water_Level_Sensor_Start_Address), unit=int(Water_Level_Sensor_Device_Id))
            print(Water_Level_Reading.registers)
    except Exception as e:
        return Ethernet_Network_Error


Water_Level_Reading()
