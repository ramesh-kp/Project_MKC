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
GatewayIpAddress = "GatewayIpAddress"
GatewayPort = "GatewayPort"
GatewayConfiguration = {
    "GatewayIpAddress": "192.168.1.254",
    "GatewayPort": 502
}

# Path
BASE_DIR = r'/home/pimkc/Desktop/Wiras/After_First_Review_26_7'

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
    "MKC28": "127"
}


# Time Configurations
UTCLocalTime = "Local_Time"


# file Configurations
SensorReadingsCreateNewFile = "Sensor_Readings_{}.json"
FunctionError = "Function_Error.log"
SensorsError = "{}_Error.log"

# Messages
Device_already_exists = "Device already exists"

# File paths
Configurations_File = "Configurations_and_Errors/Sensor_Configurations.json"
Sensor_Address_File = "Configurations_and_Errors/Sensor_Addresses.json"
