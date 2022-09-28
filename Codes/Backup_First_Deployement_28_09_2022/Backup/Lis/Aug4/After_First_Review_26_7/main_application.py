from Sensor_Readings.z_ph_reading import PhSensor
from Sensor_Readings.z_bod_reading import BODSensor
from Sensor_Readings.z_cod_reading import CODSensor
from Sensor_Readings.z_conductivity_reading import ConductivitySensor
from Sensor_Readings.z_energymeter_reading import EnergymeterSensor
from Sensor_Readings.z_tds_reading import TDSSensor
from Sensor_Readings.z_temperature_reading import TemperatureSensor
from Sensor_Readings.z_tss_reading import TSSSensor
from logging_info import Datalogs


if __name__ == "__main__":
    print(EnergymeterSensor().get_energymeter_reading())
    # print(EnergymeterSensor().set_energymeter_configurations({'Energymeter': [105, 9729, 10]}))
    print()

    # print(CODSensor().get_cod_reading())
    # print(CODSensor().set_cod_configurations({'COD': [105, 9729, 10]}))
    # print(CODSensor().set_slave_id(170))
    # print()

    # print(BODSensor().get_bod_reading())
    # print(BODSensor().set_bod_configurations({'BOD': [105, 9729, 10]}))
    # print()
    # print(TemperatureSensor().get_temperature_reading())
    # print()
    # print(TSSSensor().get_tss_reading())
    # print(TSSSensor().set_tss_configurations({'TSS': [105, 9729, 10]}))
    # print()
    # print(PhSensor().get_ph_reading())
    # print()
    # print(TDSSensor().get_tds_reading())
    # print(TDSSensor().set_tds_configurations({'TDS': [105, 9729, 10]}))
    # print()
    # print(ConductivitySensor().get_conductivity_reading())
    # print(ConductivitySensor().set_conductivity_configurations({'Conductivity': [105, 9729, 10]}))
    # print()
