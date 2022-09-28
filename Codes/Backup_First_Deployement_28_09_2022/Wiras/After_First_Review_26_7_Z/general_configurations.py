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

# Gateway Configurations
GatewayIpAddress = "GatewayIpAddress"
GatewayPort = "GatewayPort"
GatewayConfiguration = {
    "GatewayIpAddress": "192.168.1.254",
    "GatewayPort": 502
}

# Path
BASE_DIR = r'/home/pimkc/Desktop/Wiras/After_First_Review_26_7'

# Sensor Configurations
SensorGetDeviceID = "SensorGetDeviceID"
SensorGetData = "SensorGetData"
SensorConfigurations = {
    "SensorGetDeviceID": "{}_Device_Id_{}",
    "SensorGetData": "{}_Data"
}

# Error Configurations
ErrorMessageSensor = "ErrorMessageSensor"
ModbusErrorMessage = "ModbusErrorMessage"
PowerErrorMessage = "PowerErrorMessage"
ModbusSlaveIdErrorMessage = "ModbusSlaveIdErrorMessage"
ModbusConnectionError = "Modbus Error"
ErrorMessages = {
    "ErrorMessageSensor": "{}_Error_Message_{}",
    "ModbusErrorMessage": "Exception Response(131, 3, SlaveFailure)",
    "PowerErrorMessage": "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response received, expected at least 8 bytes (0 received)",
    "ModbusSlaveIdErrorMessage": "Exception Response(131, 3, GatewayPathUnavailable)",
    "Modbus Error": "[Connection] Failed to connect[ModbusTcpClient(192.168.1.254:502)]"
}

# Sensor Names
Energymeter = "Energymeter"
COD = "COD"
BOD = "BOD"
TSS = "TSS"
Temperature = "Temperature"
PH = "PH"
TDS = "TDS"
Conductivity = "Conductivity"

# Sensor Configurations
EnergymeterDeviceID = "EnergymeterDeviceID"
EnergymeterCkwh = "EnergymeterCkwh"
EnergymeterCkah = "EnergymeterCkah"
EnergymeterVoltage = "EnergymeterVoltage"
EnergymeterPowerFactorLine1 = "EnergymeterPowerFactorLine1"
EnergymeterPowerFactorLine2 = "EnergymeterPowerFactorLine2"
EnergymeterPowerFactorLine3 = "EnergymeterPowerFactorLine3"
EnergymeterTotalPowerFactor = "EnergymeterTotalPowerFactor"
EnergymeterFrequency = "EnergymeterFrequency"
# EnergymeterConfiguration = {
#     "EnergymeterDeviceID": "Energymeter_Device_ID",
#     "EnergymeterCkwh": "Energymeter_Ckwh",
#     "EnergymeterCkah": "Energymeter_Ckah",
#     "EnergymeterVoltage": "Energymeter_Voltage",
#     "EnergymeterPowerFactorLine1": "Energymeter_Power_Factor_Line_1",
#     "EnergymeterPowerFactorLine2": "Energymeter_Power_Factor_Line_2",
#     "EnergymeterPowerFactorLine3": "Energymeter_Power_Factor_Line_3",
#     "EnergymeterTotalPowerFactor": "Energymeter_Total_Power_Factor",
#     "EnergymeterFrequency": "Energymeter_Frequency"
# }


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
SensorReadingsCreateNewFile = "SensorReadingsCreateNewFile"
FunctionError = "FunctionError"
SensorsError = "SensorsError"

FileConfigurations = {
    "SensorReadingsCreateNewFile": "Sensor_Readings_{}.json",
    "FunctionError": "Function_Error.log",
    "SensorsError": "{}_Error.log"
}
