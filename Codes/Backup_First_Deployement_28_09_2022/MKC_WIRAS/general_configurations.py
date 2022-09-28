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
GATEWAYPORT = "GatewayPort"
GatewayConfiguration = {
    "GatewayIpAddress": "192.168.1.254",
    "GatewayPort": 502
}

# IoT Configurations
SENDING_IOT_CONNECTION_STRING = "HostName=mkc-iot-hub.azure-devices.net;DeviceId=\
Embedded_Azure_Communication;SharedAccessKey=6UYksdEfFpR6RS9nvCiznB89ZdsYhNcuNKOY6Kg8R9s="
RECEIVING_IOT_CONNECTION_STRING = "Endpoint=sb://iothub-ns-mkc-iot-hu-17383143-\
0e321ed71e.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=\
CoamC5VpewflsRafv4XBI9nEkxCBJ1FJZXnBC4GUwvA=;EntityPath=mkc-iot-hub"

# Path
BASE_DIR = r'/home/pimkc/Desktop/MKC_WIRAS'
DIR_PATH = r'/home/pimkc/Desktop/MKC_WIRAS/Sensor_Data_Logging'
FILEPATH = "Configurations_and_Errors/Error_Messages.json"

#Topic Name
MKC_WIRAS_SENSOR_DATA = "MKC_WIRAS_SENSOR_DATA"
MKC_WIRAS_CONFIGURATION = "MKC_WIRAS_CONFIGURATION"
MKC_WIRAS_CONFIGURATION_ACK = "MKC_WIRAS_CONFIGURATION_ACK"

# MQTT Configurations
COMMAND_TYPE = "30"
Variable_Header_Sensor_Data = format(len(MKC_WIRAS_SENSOR_DATA), "08x") + MKC_WIRAS_SENSOR_DATA
Variable_Header_Configuration_Ack = format(len(MKC_WIRAS_CONFIGURATION_ACK), "08x") +\
MKC_WIRAS_CONFIGURATION_ACK

# Sensor Configurations
SENSORGETDEVICEID = "{}_Device_ID_{}"
SENSORGETDATA = "{}_Data_{}"
SENSORGETADDRESS = "{}_Device_Address_{}"
SENSORGETSTARTADDRESS = "{}_Start_Address_{}"
SENSORGETDEFAULTID = "{}_Default_ID_{}"
SENSORGETREGISTERCOUNTS = "{}_Register_Counts_{}"

# Error Configurations
ERRORMESSAGESENSOR = "{}_Error_Message_{}"
MODBUSERRORMESSAGE = "Exception Response(131, 3, SlaveFailure)"
POWERERRORMESSAGE = "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response\
received, expected atleast 8 bytes (0 received)"
MODBUSSLAVEIDERRORMESSAGE = "Exception Response(131, 3, GatewayPathUnavailable)"
MODBUSCONNECTIONERROR = "[Connection] Failed to connect[ModbusTcpClient(192.168.1.254:502)]"


# Sensor Names
ENERGYMETER = "Energymeter"
COD = "COD"
BOD = "BOD"
TSS = "TSS"
TEMPERATURE = "Temperature"
PH = "Ph"
TDS = "TDS"
CONDUCTIVITY = "Conductivity"

# Sensor Configurations
ENERGYMETERDEVICEID = "Energymeter_Device_ID_{}"
ENERGYMETERCKWH = "Energymeter_Ckwh_{}"
ENERGYMETERCKAH = "Energymeter_Ckah_{}"
ENERGYMETERVOLTAGE = "Energymeter_Voltage_{}"
ENERGYMETERPOWERFACTORLINE1 = "Energymeter_Power_Factor_Line_1_{}"
ENERGYMETERPOWERFACTORLINE2 = "Energymeter_Power_Factor_Line_2_{}"
ENERGYMETERPOWERFACTORLINE3 = "Energymeter_Power_Factor_Line_2_{}"
ENERGYMETERTOTALPOWERFACTOR = "Energymeter_Power_Factor_Line_3_{}"
ENERGYMETERFREQUENCY = "Energymeter_Frequency_{}"
SENSORCONFIGURATIONS = "{}_Configurations"

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
CONNECTIONEXCEPTION = "ConnectionException"

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
#Error Number
Error_number ={
    "FileNotFoundError":111,
    "AttributeError":112,
    "IndexError":113,
    "ValueError":114,
    "ConnectionFailedError":115
}
FILENOTFOUND = "FileNotFoundError"
ATTRIBUTEERROR = "AttributeError"
INDEXERROR = "IndexError"
VALUEERROR = "ValueError"
CONNECTIONFAILED = "ConnectionFailedError"

ENERGYMETER_SENSOR_NOT_FOUND = "ENERGYMETER DeviceID {} Not found"
BOD_SENSOR_NOT_FOUND = "BOD DeviceID {} Not found"
COD_SENSOR_NOT_FOUND = "COD DeviceID {} Not found"
CONDUCTIVITY_SENSOR_NOT_FOUND = "CONDUCTIVITY DeviceID {} Not found"
PH_SENSOR_NOT_FOUND = "PH DeviceID {} Not found"
TDS_SENSOR_NOT_FOUND = "TDS DeviceID {} Not found"
TEMPERATURE_SENSOR_NOT_FOUND = "TEMPERATURE DeviceID {} Not found"
TSS_SENSOR_NOT_FOUND = "TSS DeviceID {} Not found"
# Time Configurations
UTCLOCALTIME = "Local_Time"


# file Configurations
SENSORREADINGSCREATENEWFILE = "{}/Sensor_Readings_{}.json"
SENSORDATALOGGING = "Sensor_Data_Logging/{}"
SENSOREADINGSEXTERNAL = "Sensor_Readings_External/{}"
FUNCTIONERROR = "Function_Error.log"
SENSORSERROR = "{}_{}.log"

# Messages
DEVICE_ALREADY_EXISTS = "Device already exists"
SEND_MESSAGE = "Sending message: {}"
MESSAGE_SUCCESSFULLY_SENT = "Message_successfully_sent"
READING_DISABLED = "Reading disabled"
ADDED_DEVICE_SUCCESSFULLY = "Added device successfully"
CONFIGURATIONS_ADDED_SUCCESSFULLY = "Configurations added successfully"
RECEIVED_READINGS_FROM_SENSOR = "Received readings from Sensor"
ERROR_IN_ENABLE_READING = "Error in enable_reading"
ERROR_IN_SET_ENERGYMETER_CONFIGURATIONS = "Error_in_set_energymeter_configurations"
ERROR_IN_SET_BOD_CONFIGURATIONS = "Error_in_set_bod_configurations"
ERROR_IN_SET_COD_CONFIGURATIONS = "Error_in_set_cod_configurations"
ERROR_IN_SET_CONDUCTIVITY_CONFIGURATIONS = "Error_in_set_conductivity_configurations"
ERROR_IN_SET_PH_CONFIGURATIONS = "Error_in_set_ph_configurations"
ERROR_IN_SET_TDS_CONFIGURATIONS = "Error_in_set_tds_configurations"
ERROR_IN_SET_TEMPERATURE_CONFIGURATIONS = "Error_in_set_temperature_configurations"
ERROR_IN_SET_TSS_CONFIGURATIONS = "Error_in_set_tss_configurations"
ERROR_IN_IOTHUB_CLIENT_SEND_MESSAGE = "Error_in_iothub_client_send_message"
READINGS_WRITTEN_TO_FILE = "Readings written to file."
NEW_CONFIGURATIONS_ADDED_TO_FILE = "New configurations added to the file"
CONFIGURATIONS_REMOVED_SUCCESSFULLY = "Configurations removed successfully"
SENSOR_READINGS_SEND_TO_IOT = "Sensor readings send to Iot"
UNABLE_TO_ADD_DEVICE = "Unable to add Device"

# File paths
CONFIGURATIONS_FILE = "Configurations_and_Errors/Sensor_Configurations.json"
SENSOR_ADDRESS_FILE = "Configurations_and_Errors/Sensor_Addresses.json"

# Global constants
FILE_SIZE = 500
WRITE_MODE = "w"
READ_MODE = "r"
READ_WRITE_MODE = "r+"
BOD_ARRAY_POS_1 = 4
BOD_ARRAY_POS_2 = 5
COD_ARRAY_POS_1 = 2
COD_ARRAY_POS_2 = 3
CONDUCTIVITY_ARRAY_POS_1 = 0
CONDUCTIVITY_ARRAY_POS_2 = 1
PH_ARRAY_POS_1 = 2
PH_ARRAY_POS_2 = 3
TDS_ARRAY_POS_1 = 2
TDS_ARRAY_POS_2 = 3
TEMPERATURE_ARRAY_POS_1 = 0
TEMPERATURE_ARRAY_POS_2 = 1
TSS_ARRAY_POS_1 = 0
TSS_ARRAY_POS_2 = 1
POSITION_1 = 0
POSITION_2 = 1

NO_OF_LOG_FILES = 5
SENSOR_READINGS = "None"
LAST_POSITION = -1
IOT = "Iot"
FUNCTION = "Function"
LINE_NUMBER_0 = 0
LINE_NUMBER_300 = 300
LINE_NUMBER_1 = 1
INITIAL_INDEX = 3
FINAL_INDEX = -3
UNDERSCORE = "_"
DOT = "."
INDENT_LEVEL = 4
FOLDER_NAME = 'Logs'
CONNECTION_COUNT_0 = 0
CONNECTION_COUNT_10 = 10
INCREMENT_1 = 1
ARRAY_POSITION_0 = 0
ARRAY_POSITION_1 = 1
ARRAY_POSITION_2 = 2
INDEX_POSITION_0 = 0
INDEX_POSITION_1 = 1
INDEX_POSITION_2 = 2
COUNT_0 = 0
POSTION_0 = 0
INITIAL_KEY_INDEX = 0
FINAL_KEY_INDEX = -1
MIN_FILE_SIZE = 2
MIN_NO_FILE = 1
ZEORES_FILL = 4
DIGITS_2 = 2
JOIN_POSITION_2 = '02x'
REPLACE_VALUE = '0x'
HEX_POSITION_0 = 0
FORMAT_LENGTH = "08x"
FLAG_STATUS_0 = False
FLAG_STATUS_1 = True
HEADER_1 =  "-------------------start-------------------"
HEADER_2 = "-------------------Stop-------------------"
FILE_CREATED_AT = " File created at "
LOG_WRITTEN = " Log is written to :"
DEVICE_INFO = " for the deviceid "
NEW_LINE = '\n'
#Log level Name
DEBUG = "Debug"
INFO = "Info"
WARNING = "Warning"
ERROR = "Error"
CRITICAL = "Critical"
Log_levels = {"Debug":10, "Info":20, "Warning":30, "Error": 40, "Critical":50}

#Error in functions
ERROR_CODE_FORMATTER = "{} - {}"
