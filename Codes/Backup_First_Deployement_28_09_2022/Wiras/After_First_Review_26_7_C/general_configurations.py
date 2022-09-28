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
GatewayConfiguration = {
    "GatewayIpAddress": "192.168.1.254",
    "GatewayPort": 502
}

# Path
BASE_DIR = "/Desktop/Wiras/After_First_Review_26_7"

# Sensor Configurations
SensorConfigurations = {
    "SensorGetDeviceID": "{}_Device_Id",
    "SensorGetData": "{}_Data"
}

# Error Configurations
ErrorMessages = {
    "ErrorMessageSensor": "{}_Error_Message",
    "ModbusErrorMessage": "Exception Response(131, 3, SlaveFailure)",
    "PowerErrorMessage": "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response received, expected\
        at least 8 bytes (0 received)",
    "ModbusError": "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response received, expected at\
        least 8 bytes (0 received)",
    "ModbusSlaveIdErrorMessage": "Exception Response(131, 3, GatewayPathUnavailable)"
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
EnergymeterConfiguration = {
    "EnergymeterDeviceID": "Energymeter_Device_ID",
    "EnergymeterCkwh": "Energymeter_Ckwh",
    "EnergymeterCkah": "Energymeter_Ckah",
    "EnergymeterVoltage": "Energymeter_Voltage",
    "EnergymeterPowerFactorLine1": "Energymeter_Power_Factor_Line_1",
    "EnergymeterPowerFactorLine2": "Energymeter_Power_Factor_Line_2",
    "EnergymeterPowerFactorLine3": "Energymeter_Power_Factor_Line_3",
    "EnergymeterTotalPowerFactor": "Energymeter_Total_Power_Factor",
    "EnergymeterFrequency": "Energymeter_Frequency"
}

# Error Definitions
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
}


# Time Configurations
UTCLocalTime = "Local_Time"


# file Configurations
FileConfigurations = {
    "SensorReadingsCreateNewFile": "Sensor_Readings_{}.json",
    "FunctionError": "Function_Error.log",
    "SensorsError" : "{}_Error.log"
}
