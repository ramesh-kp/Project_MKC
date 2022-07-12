# IoT Configurations
Sending_Iot_Connection_String = "HostName=mkc-iot-hub.azure-devices.net;DeviceId=sensors_001;SharedAccessKey=rEp4wNLKN/WybUfQLhLmiWmzcpga68RIGO2nTudNeYU="
Receiving_Iot_Connection_String = "Endpoint=sb://iothub-ns-mkc-iot-hu-17383143-0e321ed71e.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=CoamC5VpewflsRafv4XBI9nEkxCBJ1FJZXnBC4GUwvA=;EntityPath=mkc-iot-hub"
General_Configuration_File = "General_Configuration.py"
Sensor_Configuration_File = "Sensor_Configuration.json"
Sensor_Reading_File = "Sensor_Readings_0.json"

# Gateway Configurations
Gateway_Ip_Address = "192.168.1.254"
Gateway_Port = 502

# Error Configurations
Modbus_Error_Message = "Exception Response(131, 3, SlaveFailure)"
Modbus_Error = {"Error_Message": "Error in Data"}
Modbus_Slave_Id_Error_Message = "Exception Response(131, 3, GatewayPathUnavailable)"
Modbus_Slave_Id_Error = {"Error_Message": "Error in Slave Id"}
Power_Error_Message = "Modbus Error: [Input/Output] Modbus Error: [Invalid Message] No response received, expected at least 8 bytes (0 received)"
Power_Error = {"Error_Message": "Error in Connection"}
Ethernet_Network_Error = {"Error_Message": "Error in Ethernet Network"}
Network_Connection_Error = {"Error_Message": "Error in Network Connection"}

Validation_Error = {
    "MKC1": 101,
    "MKC2": 102,
    "MKC3": 103,
    "MKC4": 104,
    "MKC5": 105,
    "MKC6": 106,
    "MKC7": 107,
    "MKC8": 113,
    "MKC9": 114,
    "MKC10": 115,
    "MKC11": 116,
    "MKC12": 117,
    "MKC13": 118,
    "MKC14": 119
}


# Log Configurations
Log_Send_File = "send_data_file.log"
Log_Receive_File = "receive_data_file.log"
Log_Error_File = "error_data_file.log"

# Device Configurations
Pi_Id = "PI01"
Router_Id = "RT01"
Gateway_Id = "GW01"
Device_Id = {"Pi_Id": Pi_Id, "Router_Id": Router_Id, "Gateway_Id": Gateway_Id}

# MQTT Configurations
Command_Type = "30"
Topic = "MKC_WIRAS_SENSOR_DATA"
Variable_Header = format(len(Topic), "08x") + Topic
