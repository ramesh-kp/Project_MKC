"This document consist of functions which manages the sensor functions."
from Sensor_Readings.ph_reading import PhSensor
from Sensor_Readings.bod_reading import BODSensor
from Sensor_Readings.cod_reading import CODSensor
from Sensor_Readings.conductivity_reading import ConductivitySensor
from Sensor_Readings.energymeter_reading import EnergymeterSensor
from Sensor_Readings.tds_reading import TDSSensor
from Sensor_Readings.temperature_reading import TemperatureSensor
from Sensor_Readings.tss_reading import TSSSensor
from Utilities.util_time import LocalTime
from logging_info import Datalogs
from File_Management.sensor_data_logging import DeviceDataLogging
from Sensor_Readings.bod_reading import bod_start_flag
import time
result = {}


if __name__ == "__main__":
    local_time = LocalTime().get_local_time()
    result.update(local_time)

    # energymeter_data = EnergymeterSensor().get_energymeter_reading()
    # result.update(energymeter_data)
    # DeviceDataLogging().sensor_readings_log(result)
    # EnergymeterSensor().remove_energymeter_configurations(171,energymeter_flag_check)
    # print(EnergymeterSensor().set_energymeter_configurations({'Energymeter': [172, 1, 46]}))
    # print()

    bod_data = BODSensor().get_bod_reading(bod_start_flag)
    result.update(bod_data)
    bod_flag_check = DeviceDataLogging().sensor_readings_log(result)
    # BODSensor().remove_bod_configurations(101, bod_flag_check)
    # print("bod_start_flag",bod_start_flag)
    # BODSensor().bod_reinitiliaze(bod_start_flag)
    # print(BODSensor().set_bod_configurations({'BOD': [101, 9729, 10]}))
    # print()

    # cod_data = CODSensor().get_cod_reading()
    # result.update(cod_data)
    # print(result)
    # cod_flag_check = DeviceDataLogging().sensor_readings_log(result)
    # CODSensor().remove_cod_configurations(102, cod_flag_check)
    # print(CODSensor().set_cod_configurations({'COD': [101, 9729, 10]}))

    # print()

    # temperature_data = TemperatureSensor().get_temperature_reading()
    # result.update(temperature_data)
    # DeviceDataLogging().sensor_readings_log(result)
    # TemperatureSensor().remove_temperature_configurations(101, temperature_flag_check)
    # print(TemperatureSensor().set_temperature_configurations(
    #     {'Temperature': [101, 9729, 10]}))
    # print()

    # tss_data = TSSSensor().get_tss_reading()
    # result.update(tss_data)
    # DeviceDataLogging().sensor_readings_log(result)
    # TSSSensor().remove_tss_configurations(101, tss_flag_check)
    # print(TSSSensor().set_tss_configurations({'TSS': [101, 9729, 10]}))
    # print()

    # ph_data = PhSensor().get_ph_reading()
    # result.update(ph_data)
    # DeviceDataLogging().sensor_readings_log(result)
    # PhSensor().remove_ph_configurations(111,ph_flag_check)
    # print(PhSensor().set_ph_configurations({'Ph': [112, 9729, 10]}))
    # print()


    # tds_data = TDSSensor().get_tds_reading()
    # result.update(tds_data)
    # DeviceDataLogging().sensor_readings_log(result)
    # TDSSensor().remove_tds_configurations(121,tds_flag_check)
    # print(TDSSensor().set_tds_configurations({'TDS': [122, 9729, 10]}))
    # print()

    # conductivity_data = ConductivitySensor().get_conductivity_reading()
    # result.update(conductivity_data)
    # DeviceDataLogging().sensor_readings_log(result)
    # ConductivitySensor().remove_conductivity_configurations(121,tds_flag_check)
    # print(ConductivitySensor().set_conductivity_configurations(
    #     {'Conductivity': [122, 9729, 10]}))
    # print()
