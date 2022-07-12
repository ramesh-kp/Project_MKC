from pymodbus.client.sync import ModbusTcpClient

Gateway_Ip_Address = "192.168.1.254"
Gateway_Port = 502

TDS_Device_Id = 120
TDS_Start_Address = 9729
TDS_Register_Counts = 4


def Gateway_Connect():
    gateway_client = ModbusTcpClient(Gateway_Ip_Address, int(Gateway_Port))
    gateway_client.connect()
    return gateway_client


def little_to_big(number):
    hex_number = hex(int(number)).replace('0x', '').zfill(4)
    converted_number = bytearray.fromhex(hex_number)
    converted_number.reverse()
    little_indian_number = ''.join(format(x, '02x')
                                   for x in converted_number).upper()
    real_number = int(little_indian_number, 16)
    return real_number


def Set_Slave_ID(default, number):
    try:
        print("hi")
        res = ModbusTcpClient(Gateway_Ip_Address, int(
            Gateway_Port)).write_registers(address=12288, values=little_to_big(number), unit=int(default))
        # address - Starting Address
        # values - Values to write
        # unit - Current Slave Id
        print(res)
    except Exception as e:
        print(e)


def Slave_ID_Number():
    try:
        id = Gateway_Connect().read_holding_registers(count=15, address=12289, unit=120)
        first_digit = hex(id.registers[0])
        first_digit = first_digit[2:]
        ab = bytearray.fromhex(first_digit)
        ab.reverse()
        bc = ''.join(format(x, '02x') for x in ab).upper()
        Reading = int(bc, 16)
        print(Reading)
    except Exception as e:
        print(e)


Slave_ID_Number()
Set_Slave_ID("120", "120")
