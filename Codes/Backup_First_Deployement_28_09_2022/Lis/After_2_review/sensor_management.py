"This document consist of functions which manages the sensor functions."
# from azure.iot.device import IoTHubDeviceClient
# from IOT_Communication.Iot_hub_communication import Iotconnection
# from Sensor_Management.ph_sensor_management import PhSensor
# from Sensor_Management.bod_sensor_management import BODSensor
# from Sensor_Management.cod_sensor_management import CODSensor
# from Sensor_Management.conductivity_sensor_management import ConductivitySensor
# from Sensor_Management.energymeter_sensor_management import EnergymeterSensor
# from Sensor_Management.tds_sensor_management import TDSSensor
# from Sensor_Management.temperature_sensor_management import TemperatureSensor
# from Sensor_Management.tss_sensor_management import TSSSensor
from logging_info import Datalogs
# from Utilities.util_time import LocalTime
# from Utilities.util_error_mapping import Matching
# from general_configurations import FILE_NOT_FOUND, INFO_NOT_FOUND
# from logging_info import Datalogs
# from File_Management.sensor_data_logging import DeviceDataLogging
# from general_configurations import Sending_Iot_Connection_String, SENSORDATALOGGING
# import time
# result = {}

# IotHub_client = IoTHubDeviceClient.create_from_connection_string(
#     Sending_Iot_Connection_String)
# if __name__ == "__main__":
#     local_time = LocalTime().get_local_time()
#     result.update(local_time)
#     result.update(BODSensor(100).enable_reading())
#     print(result)
    # reading_mode = DeviceDataLogging().set_mode(False)
    # DeviceDataLogging().sensor_readings_log(result, reading_mode)
#     # BODSensor(101).remove_bod_configurations()

# result = BODSensor(101).set_bod_configurations({'BOD': [101, 9729]})
# print(result)
    # Iotconnection().send_sensor_readings(IotHub_client)




# Iotconnection().send_sensor_readings(IotHub_client)
# Iotconnection().check()
# DeviceDataLogging().file_created(0,"Sensor_Data_Logging")

# result = BODSensor(101).remove_bod_configurations()
# print(result)
# BODSensor().enable_reading()



# results = BODSensor(101).set_bod_configurations({'BOD': [101, 9729, 10]})
# print(results)

Datalogs().logging_error("Hello", "sam.log", 20)
