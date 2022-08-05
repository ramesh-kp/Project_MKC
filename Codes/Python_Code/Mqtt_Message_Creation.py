azure_message = str({"Time": 2, "Energymeter": [
    170, 1, 46], "COD": [100, 9729, 10], "BOD": [100, 9729, 10], "Temperature": [100, 9729, 10], "TSS": [100, 4608, 4], "Ph": [110, 9729, 5], "TDS": [120, 9729, 4], "Conductivity": [120, 9729, 4]})
# azure_message = str({"Time": 10})
# azure_message = str({"RESET": "Clear"})
# azure_message = str({"TDS": [120, 9729, 4]})
Command_Type = "30"
Topic = "MKC_WIRAS_CONFIGURATION"
Variable_Header = format(len(Topic), "08x") + Topic
MQTT_Message = Variable_Header + \
    format(len(azure_message), "08x") + azure_message
Total_Length = format(len(MQTT_Message), "08x")
real_data = Command_Type + Total_Length + MQTT_Message
print(real_data)
