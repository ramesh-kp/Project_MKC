#------------------------------------------------------------------------#
# Created by  : Ramesh K P
# Employee ID : 15265
# Created Date: 31/05/2022
# Description : This file contains configuration values
# Modified Date: 26/07/2022
# Modified By  : Lis Sebastian
# Employee ID  : 15282
# Modification :
#------------------------------------------------------------------------#
"""
This file contains configuration values
"""
# Gateway Configurations
from turtle import position


GatewayIpAddress = "GatewayIpAddress"
GatewayPort = "GatewayPort"
GatewayConfiguration = {
    "GatewayIpAddress": "192.168.1.254",
    "GatewayPort": 502
}

# IoT Configurations
Sending_Iot_Connection_String = "HostName=mkc-iot-hub.azure-devices.net;DeviceId=Embedded_Azure_Communication;\
SharedAccessKey=6UYksdEfFpR6RS9nvCiznB89ZdsYhNcuNKOY6Kg8R9s="
Receiving_Iot_Connection_String = "Endpoint=sb://iothub-ns-mkc-iot-hu-17383143-0e321ed71e.servicebus.windows.net/;\
SharedAccessKeyName=iothubowner;SharedAccessKey=CoamC5VpewflsRafv4XBI9nEkxCBJ1FJZXnBC4GUwvA=;EntityPath=mkc-iot-hub"

# Path
BASE_DIR = r'/home/pimkc/Desktop/Wiras/After_First_Review_26_7'
DIR_PATH = r'/home/pimkc/Desktop/Wiras/After_First_Review_26_7/Sensor_Data_Logging'
filepath = "Configurations_and_Errors/Error_Messages.json"

#Topic Name
MKC_WIRAS_SENSOR_DATA = "MKC_WIRAS_SENSOR_DATA"
MKC_WIRAS_CONFIGURATION = "MKC_WIRAS_CONFIGURATION"
MKC_WIRAS_CONFIGURATION_ACK = "MKC_WIRAS_CONFIGURATION_ACK"

# MQTT Configurations
Command_Type = "30"
Variable_Header_Sensor_Data = format(len(MKC_WIRAS_SENSOR_DATA), "08x") + MKC_WIRAS_SENSOR_DATA
Variable_Header_Configuration_Ack = format(len(MKC_WIRAS_CONFIGURATION_ACK), "08x") + MKC_WIRAS_CONFIGURATION_ACK

# Sensor Configurations
SensorGetDeviceID = "{}_Device_ID_{}"
SensorGetData = "{}_Data_{}"
SensorGetAddress = "{}_Device_Address_{}"
SensorGetStartAddress = "{}_Start_Address_{}"
SensorGetDefaultID = "{}_Default_ID_{}"
SensorGetRegisterCounts = "{}_Register_Counts_{}"

# Error Configurations
ErrorMessageSensor = "{}_Error_Message_{}"
ModbusErrorMessage = "Exception Response(131, 3, SlaveFailure)"
PowerErrorMessage = "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response received, expected at\
    least 8 bytes (0 received)"
ModbusSlaveIdErrorMessage = "Exception Response(131, 3, GatewayPathUnavailable)"
ModbusConnectionError = "[Connection] Failed to connect[ModbusTcpClient(192.168.1.254:502)]"

# Sensor Names
Energymeter = "Energymeter"
COD = "COD"
BOD = "BOD"
TSS = "TSS"
Temperature = "Temperature"
PH = "Ph"
TDS = "TDS"
Conductivity = "Conductivity"

# Sensor Configurations
EnergymeterDeviceID = "Energymeter_Device_ID_{}"
EnergymeterCkwh = "Energymeter_Ckwh_{}"
EnergymeterCkah = "Energymeter_Ckah_{}"
EnergymeterVoltage = "Energymeter_Voltage_{}"
EnergymeterPowerFactorLine1 = "Energymeter_Power_Factor_Line_1_{}"
EnergymeterPowerFactorLine2 = "Energymeter_Power_Factor_Line_2_{}"
EnergymeterPowerFactorLine3 = "Energymeter_Power_Factor_Line_2_{}"
EnergymeterTotalPowerFactor = "Energymeter_Power_Factor_Line_3_{}"
EnergymeterFrequency = "Energymeter_Frequency_{}"
SensorConfigurations = "{}_Configurations"

# Error Definitions
MKC1 = "MKC1"
MKC2 = "MKC2"
MKC3 = "MKC3"
MKC4 = "MKC4"
MKC5 = "MKC5"
MKC6 = "MKC6"
MKC7 = "MKC7"
MKC8 = "MKC8"
MKC9 = "MKC9"
MKC10 = "MKC10"
MKC11 = "MKC11"
MKC12 = "MKC12"
MKC13 = "MKC13"
MKC14 = "MKC14"
MKC15 = "MKC15"
MKC16 = "MKC16"
MKC17 = "MKC17"
MKC18 = "MKC18"
MKC19 = "MKC19"
MKC20 = "MKC20"
MKC21 = "MKC21"
MKC22 = "MKC22"
MKC23 = "MKC23"
MKC24 = "MKC24"
MKC25 = "MKC25"
MKC26 = "MKC26"
MKC27 = "MKC27"
MKC28 = "MKC28"
MKC29 = "MKC29"
MKC30 = "MKC30"

ValidationError = {
    "MKC1": "101",
    "MKC2": "102",
    "MKC3": "103",
    "MKC4": "104",
    "MKC5": "105",
    "MKC6": "106",
    "MKC7": "107",
    "MKC8": "113",
    "MKC9": "114",
    "MKC10": "115",
    "MKC11": "116",
    "MKC12": "117",
    "MKC13": "118",
    "MKC14": "119",
    "MKC15": "120",
    "MKC16": "121",
    "MKC17": "108",
    "MKC18": "122",
    "MKC19": "123",
    "MKC20": "124",
    "MKC21": "109",
    "MKC22": "110",
    "MKC23": "111",
    "MKC24": "112",
    "MKC25": "124",
    "MKC26": "125",
    "MKC27": "126",
    "MKC28": "127",
    "MKC29": "128",
    "MKC30": "129"
}
BOD_Sensor_not_found = "BOD DeviceID {} Not found"

# Time Configurations
UTCLocalTime = "Local_Time"


# file Configurations
SensorReadingsCreateNewFile = "{}/Sensor_Readings_{}.json"
SensorDataLogging = "Sensor_Data_Logging/{}"
SensorReadingsExternal = "Sensor_Readings_External/{}"
FunctionError = "Function_Error.log"
SensorsError = "{}.log"

# Messages
Device_already_exists = "Device already exists"
Send_Message = "Sending message: {}"
Message_successfully_sent = "Message_successfully_sent"
Reading_disabled = "Reading disabled"
Added_device_successfully = "Added device successfully"
Configurations_added_successfully = "Configurations added successfully"
Received_readings_from_Sensor = "Received readings from Sensor"
Error_in_enable_reading = "Error in enable_reading"
Error_in_set_bod_configurations = "Error_in_set_bod_configurations"
Error_in_iothub_client_send_message = "Error_in_iothub_client_send_message"
Readings_written_to_file = "Readings written to file."

# File paths
Configurations_File = "Configurations_and_Errors/Sensor_Configurations.json"
Sensor_Address_File = "Configurations_and_Errors/Sensor_Addresses.json"

# Global constants
file_size = 20000
write_mode = "w"
read_mode = "r"
read_write_mode = "r+"
bod_position_1 = 2
bod_position_2 = 3
No_of_log_files = 2
Sensor_readings = "None"
last_position = -1
Iot = "Iot"
Function = "Function"
line_number_0  = 0
line_number_300 = 300
line_number_1 = 1
final_index = -3
underscore = "_"
dot = "."
indent_level = 4
Folder_name = 'Logs'

#Log level Name
Debug = "Debug"
Info = "Info"
Warning = "Warning"
Error = "Error"
Critical = "Critical"
Log_levels = {"Debug":10, "Info":20, "Warning":30, "Error": 40, "Critical":50}

#Error in functions
Error_Code_Formatter = "{} - {} - {}"


