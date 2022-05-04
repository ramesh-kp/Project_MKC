import time
import Configurations
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
print()
print("<<< Waste Water Management >>>")
client = ModbusTcpClient(Configurations.Gateway_Ip_Address,
                         Configurations.Gateway_Port)  # port=502
client.connect()
if client.connect():
    print("Connected")

Energymeter_Reading = client.read_holding_registers(
    count=Configurations.Energymeter_Register_Counts, address=Configurations.Energymeter_Start_Address, unit=Configurations.Energymeter_Device_Id)
print(Energymeter_Reading.registers)
Energymeter_Unit_Consumed = Energymeter_Reading.registers[5]/1000
print("Unit Consumed : ", Energymeter_Unit_Consumed)
print()
time.sleep(2)
client.close()
