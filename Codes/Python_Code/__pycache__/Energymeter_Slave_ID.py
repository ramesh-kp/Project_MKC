from pymodbus.client.sync import ModbusTcpClient
Modbus_Error_Message = "Exception Response(131, 3, SlaveFailure)"
Modbus_Error = {"Error_Message": "Error in Data"}
Power_Error_Message = "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response received, expected at least 8 bytes (0 received)"
Power_Error = {"Error_Message": "Error in Connection"}
Ethernet_Network_Error = {"Error_Message": "Error in Ethernet Network"}
Gateway_Ip_Address = "192.168.1.254"
Gateway_Port = 502
Energymeter_Device_Id = 170
Energymeter_Start_Address = 1
Energymeter_Register_Counts = 2


def Gateway_Connect():
    gateway_client = ModbusTcpClient(Gateway_Ip_Address, Gateway_Port)
    gateway_client.connect()
    return gateway_client


def Set_Slave_ID():
    try:
        print("hi")
        just = ModbusTcpClient(Gateway_Ip_Address, int(
            Gateway_Port)).write_register(address=2, value=170, unit=170)
        # address - Starting Address
        # values - Values to write
        # unit - Current Slave Id
        print(just)
    except Exception as e:
        print(e)


def Slave_ID_Number():
    try:
        id = Gateway_Connect().read_holding_registers(count=Energymeter_Register_Counts,
                                                      address=Energymeter_Start_Address, unit=Energymeter_Device_Id)
        print(id.registers)
        print(id.registers[1])
    except Exception as e:
        print(e)


Slave_ID_Number()
Set_Slave_ID()
