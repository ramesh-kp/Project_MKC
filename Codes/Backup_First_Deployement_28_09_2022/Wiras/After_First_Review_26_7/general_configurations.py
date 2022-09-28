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
GATEWAYIPADDRESS = "GatewayIpAddress"
GatewayPort = "GatewayPort"
GatewayConfiguration = {
    "GATEWAYIPADDRESS": "192.168.1.254",
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
INFO_NOT_FOUND = "INFO_NOT_FOUND"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
INFO_ALREADY_ADDED = "INFO_ALREADY_ADDED"
LIST_INDEX_ERROR = "LIST_INDEX_ERROR"
INVALID_INFO = "INVALID_INFO"
INVALID_SLAVE_ID = "INVALID_SLAVE_ID"
EMPTY_FILE = "EMPTY_FILE"
EMPTY_RETURN = "EMPTY_RETURN"
CONNECTION_FAILED = "CONNECTION_FAILED"
INVALID_CONFIGURATIONS = "INVALID_CONFIGURATIONS"
INVALID_DATA_FROM_MODBUS = "INVALID_DATA_FROM_MODBUS"
INVALID_TIME = "INVALID_TIME"
INFO_NOT_FOUND_IN_FILE = "INFO_NOT_FOUND_IN_FILE"
INVALID_CREDENTIALS ="INVALID_CREDENTIALS"
FAILURE_IN_CONNECTION = "FAILURE_IN_CONNECTION"
CONNECTION_LOST = "CONNECTION_LOST"
CONNECTION_TIME_OUT = "CONNECTION_TIME_OUT"
CLIENT_NOT_CONNECTED = "CLIENT_NOT_CONNECTED"

# ValidationMessage = {
#     "INFONOTFOUND": "101",
#     "FILENOTFOUND": "102",
#     "INFOALREADYADDED": "103",
#     "LISTINDEXERROR": "104",
#     "INVALIDINFO": "105",
#     "INVALIDSLAVEID": "106",
#     "EMPTYFILE": "107",
#     "MKC8": "113",
#     "MKC9": "",
#     "MKC10": "",
#     "MKC11": "",
#     "MKC12": "",
#     "MKC13": "",
#     "MKC14": "",
#     "MKC15": "",
#     "MKC16": "",
#     "MKC17": "108",
#     "MKC18": "",
#     "MKC19": "",
#     "MKC20": "",
#     "MKC21": "",
#     "MKC22": "",
#     "MKC23": "",
#     "MKC24": "",
#     "MKC25": "",
#     "MKC26": "",
#     "MKC27": "",
#     "MKC28": "127",
#     "MKC29": "128",
#     "MKC30": "129"
# }
BOD_Sensor_not_found = "BOD DeviceID {} Not found"

# Time Configurations
UTCLocalTime = "Local_Time"


# file Configurations
SensorReadingsCreateNewFile = "{}/Sensor_Readings_{}.json"
SensorDataLogging = "Sensor_Data_Logging/{}"
SensorReadingsExternal = "Sensor_Readings_External/{}"
FunctionError = "Function_Error.log"
SensorsError = "{}_{}_{}.log"

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
New_configurations_added_to_file = "New configurations added to the file"
Configurations_removed_successfully = "Configurations removed successfully"
Sensor_readings_send_to_Iot = "Sensor readings send to Iot"
Unable_to_add_Device = "Unable to add Device"

# File paths
Configurations_File = "Configurations_and_Errors/Sensor_Configurations.json"
Sensor_Address_File = "Configurations_and_Errors/Sensor_Addresses.json"

# Global constants
file_size = 200
write_mode = "w"
read_mode = "r"
read_write_mode = "r+"
bod_array_pos_1 = 2
bod_array_pos_2 = 3
bod_position_1 = 0
bod_position_2 = 1
No_of_log_files = 5
Sensor_readings = "None"
last_position = -1
Iot = "Iot"
Function = "Function"
line_number_0  = 0
line_number_300 = 300
line_number_1 = 1
initial_index = 3
final_index = -3
underscore = "_"
dot = "."
indent_level = 4
Folder_name = 'Logs'
connection_count_0 = 0
connection_count_10 = 10
increment_1 = 1
array_position_0 = 0
array_position_1 = 1
array_position_2 = 2
index_position_0 = 0
index_position_1 = 1
index_position_2 = 2
count_0 = 0
postion_0 = 0
initial_key_index = 0
final_key_index = -1
min_file_size = 2
min_no_file = 1
zeores_fill = 4
digits_2 = 2
join_position_2 = '02x'
replace_value = '0x'
hex_position_0 = 0
format_length = "08x"
flag_status_0 = False
flag_status_1 = True


#Log level Name
Debug = "Debug"
Info = "Info"
Warning = "Warning"
Error = "Error"
Critical = "Critical"
Log_levels = {"Debug":10, "Info":20, "Warning":30, "Error": 40, "Critical":50}

#Error in functions
Error_Code_Formatter = "{} - {}"


