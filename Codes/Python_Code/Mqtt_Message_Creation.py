# azure_message = str({"Time": 15, "Energymeter": [
# 171, 1, 46], "COD": [101, 9729, 10], "BOD": [101, 9729, 10], "Temperature": [101, 9729, 10], "TSS": [101, 4608, 4], "Ph": [110, 9729, 5], "TDS": [120, 9729, 4]})
azure_message = str({"Time": 4})
Command_Type = "30"
Topic = "MKCWIRAS"
Variable_Header = format(len(Topic), "08x") + Topic
MQTT_Message = Variable_Header + \
    format(len(azure_message), "08x") + azure_message
Total_Length = format(len(MQTT_Message), "08x")
real_data = Command_Type + Total_Length + MQTT_Message
print(real_data)
