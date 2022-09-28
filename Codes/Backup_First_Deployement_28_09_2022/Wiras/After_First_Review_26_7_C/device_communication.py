#------------------------------------------------------------------------#
# Created by  : Ramesh K P
# Employee ID : 15265
# Created Date: 31/05/2022
# Description : This document demonstrates the connection
#               of the sensor with raspberry pi and how to communicate sensor readings to it.
# Modified Date: 26/07/2022
# Modified By  : Lis Sebastian
# Employee ID  : 15282
# Modification : Created different class for individual sensors. Created class for Device data Logging.
#------------------------------------------------------------------------#
"""
This document demonstrates the connection of the sensor with raspberry pi and how to communicate sensor readings to it.
"""
import json
import os
import struct
from datetime import datetime, timedelta
from pymodbus.client.sync import ModbusTcpClient


from logging_info import Datalogs
# from general_configurations import *
from general_configurations import BOD, COD, PH, TDS, TSS, Conductivity, Energymeter, FileConfigurations,Temperature
from general_configurations import SensorConfigurations, ErrorMessages, EnergymeterConfiguration,ValidationError
from general_configurations import UTCLocalTime,GatewayConfiguration

result = {}
connection_checking_count = 0


class DeviceCommunication(object):
    """
    This class consist of functions which establishes the connection with gateway client and and get the local time
    """
    @classmethod
    def gateway_connect(cls):
        gateway_client = ModbusTcpClient(
            GatewayConfiguration["GatewayIpAddress"], GatewayConfiguration["GatewayPort"])
        gateway_client.connect()
        return gateway_client


class DeviceCommonFunctions(object):
    """
    This class consist of functions,get_local_time(),check_error_message(),
    which are commonly used in the below classes
    """
    @classmethod
    def get_local_time(cls):
        current_time = str(datetime.utcnow() + timedelta(minutes=330))
        time_stamp = {UTCLocalTime: current_time}
        return time_stamp

    @classmethod
    def sensor_data_show(cls, sensor, sensor_reading):
        data_result = {}
        if sensor == Energymeter:
            data_result = EnergymeterSensor().parse_rawdata_energymeter(sensor_reading.registers)
        elif sensor == COD:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor): STPSensor().CODSensor(
                    ).cod_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor): STPSensor(
                    ).parse_rawdata(sensor_reading.registers,STPSensor().CODSensor().cod_data_position[0],STPSensor(
                    ).CODSensor().cod_data_position[1])}
        elif sensor == BOD:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor): STPSensor().BODSensor(
                    ).bod_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor): STPSensor(
                    ).parse_rawdata(sensor_reading.registers,STPSensor().BODSensor().bod_data_position[0], STPSensor(
                    ).BODSensor().bod_data_position[1])}
        elif sensor == Temperature:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor):STPSensor().TemperatureSensor(
                    ).temperature_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor): STPSensor(
                    ).parse_rawdata(sensor_reading.registers,STPSensor().TemperatureSensor(
                    ).temperature_data_position[0],STPSensor().TemperatureSensor().temperature_data_position[1])}
        elif sensor == TSS:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor): STPSensor().TSSSensor(
                    ).tss_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor): STPSensor(
                    ).parse_rawdata(sensor_reading.registers,STPSensor().TSSSensor().tss_data_position[0],
                    STPSensor().TSSSensor().tss_data_position[1])}
        elif sensor == PH:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor): STPSensor().PhSensor(
                    ).ph_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor): STPSensor(
                    ).parse_rawdata(sensor_reading.registers,STPSensor().PhSensor().ph_data_position[0],
                    STPSensor().PhSensor().ph_data_position[1])}
        elif sensor == TDS:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor): STPSensor().TDSSensor(
                    ).tds_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor): STPSensor(
                    ).parse_rawdata(sensor_reading.registers,STPSensor().TDSSensor().tds_data_position[0], STPSensor(
                    ).TDSSensor().tds_data_position[1])}
        elif sensor == Conductivity:
            data_result = {SensorConfigurations["SensorGetDeviceID"].format(sensor):STPSensor().ConductivitySensor(
                    ).conductivity_configurations[0][0],SensorConfigurations["SensorGetData"].format(sensor):
                    round(STPSensor().parse_rawdata(sensor_reading.registers,STPSensor().ConductivitySensor(
                    ).conductivity_data_position[0],STPSensor().ConductivitySensor(
                    ).conductivity_data_position[1])/10, 2)}
        return data_result

    @classmethod
    def check_error_message(cls, sensor, sensor_reading):
        global connection_checking_count
        sensor_result = {}
        sensor_reading_check = str(sensor_reading)
        if sensor_reading_check == ErrorMessages["PowerErrorMessage"]:
            sensor_result.update(
                {ErrorMessages["ErrorMessageSensor"].format(sensor): ValidationError["MKC22"]})
            Datalogs().logging_error(
                ValidationError["MKC22"], FileConfigurations["SensorsError"].format(sensor))
        if sensor_reading_check == ErrorMessages["ModbusErrorMessage"]:
            connection_checking_count = connection_checking_count+1
            if connection_checking_count == 10:
                connection_checking_count = 0
                sensor_result.update(
                    {ErrorMessages["ErrorMessageSensor"].format(sensor): ValidationError["MKC17"]})
                Datalogs().logging_error(
                    ValidationError["MKC17"], FileConfigurations["SensorsError"].format(sensor))
            else:
                sensor_result.update({"None": None})
        elif sensor_reading_check == ErrorMessages["ModbusSlaveIdErrorMessage"]:
            sensor_result.update(
                {ErrorMessages["ErrorMessageSensor"].format(sensor): ValidationError["MKC21"]})
            Datalogs().logging_error(
                ValidationError["MKC21"], FileConfigurations["SensorsError"].format(sensor))
        else:
            sensor_result.update(DeviceCommonFunctions(
            ).sensor_data_show(sensor, sensor_reading))
        return sensor_result


class EnergymeterSensor(object):
    """
    This class consist of functions in relation with the Energymeter Sensor.
    """

    def __init__(self):
        self.configurations = [[170, 1, 46]]

    @classmethod
    def parse_rawdata_energymeter(cls, energymeter_reading_raw):
        slave_id = energymeter_reading_raw[1]
        ckwh = energymeter_reading_raw[5] / 1000
        ckah = energymeter_reading_raw[7] / 1000
        voltage = energymeter_reading_raw[9] / 10
        power_factor_line_1 = energymeter_reading_raw[33] / 100
        power_factor_line_2 = energymeter_reading_raw[35] / 100
        power_factor_line_3 = energymeter_reading_raw[37] / 100
        total_power_factor = energymeter_reading_raw[43] / 100
        frequency = energymeter_reading_raw[45] / 10
        energy_meter_data = {
            EnergymeterConfiguration["EnergymeterDeviceID"]: slave_id,
            EnergymeterConfiguration["EnergymeterCkwh"]: ckwh,
            EnergymeterConfiguration["EnergymeterCkah"]: ckah,
            EnergymeterConfiguration["EnergymeterVoltage"]: voltage,
            EnergymeterConfiguration["EnergymeterPowerFactorLine1"]: power_factor_line_1,
            EnergymeterConfiguration["EnergymeterPowerFactorLine2"]: power_factor_line_2,
            EnergymeterConfiguration["EnergymeterPowerFactorLine3"]: power_factor_line_3,
            EnergymeterConfiguration["EnergymeterTotalPowerFactor"]: total_power_factor,
            EnergymeterConfiguration["EnergymeterFrequency"]: frequency,
        }
        return energy_meter_data

    def get_energymeter_reading(self):
        try:
            for pos in range(len(self.configurations)):
                while True:
                    energymeter_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.configurations[pos][2],
                        address=self.configurations[pos][1],
                        unit=self.configurations[pos][0]))
                    energymeter_output = DeviceCommonFunctions().check_error_message(
                        Energymeter, energymeter_reading)
                    if None not in energymeter_output.values():
                        return energymeter_output
        except Exception as e:
            print("ERROR:::::", e)


class STPSensor(object):
    """
    This class consist of functions in relation with Stp Sensors and this functions are common functions which are used
    in each sensor class
    """
    @classmethod
    def little_to_big_endian(cls, input_str):
        hex_string = bytearray.fromhex(input_str)
        hex_string.reverse()
        return ''.join(format(x, '02x') for x in hex_string).upper()

    def parse_rawdata(self, sensor_raw_data, data_pos_1, data_pos_2):
        raw_data_hex_1 = hex(sensor_raw_data[data_pos_1]).replace(
            '0x', '').zfill(4)
        raw_data_hex_2 = hex(sensor_raw_data[data_pos_2]).replace(
            '0x', '').zfill(4)
        first_post_hex = self.little_to_big_endian(
            raw_data_hex_1 + raw_data_hex_2)
        sensor_reading = round(struct.unpack(
            '!f', bytes.fromhex(first_post_hex))[0], 2)
        return sensor_reading

    class CODSensor(object):
        """
        This class consist of functions which initilize the cod_configurations and get the readings from COD Sensor.
        """

        def __init__(self):
            self.cod_configurations = [[100, 9729, 10]]
            self.cod_data_position = [2, 3]

        def get_cod_reading(self):
            try:
                for pos in range(len(self.cod_configurations)):
                    cod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.cod_configurations[pos][2],
                        address=self.cod_configurations[pos][1],
                        unit=self.cod_configurations[pos][0]))
                    cod_output = DeviceCommonFunctions().check_error_message(COD, cod_reading)
                    if None not in cod_output.values():
                        return cod_output
            except Exception as ex:
                print(ex)

    class BODSensor(object):
        """
        This class consist of functions which initilize the bod_configurations and get the readings from BOD Sensor.
        """

        def __init__(self):
            self.bod_configurations = [[100, 9729, 10]]
            self.bod_data_position = [4, 5]

        def get_bod_reading(self):
            try:
                for pos in range(len(self.bod_configurations)):
                    bod_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.bod_configurations[pos][2],
                        address=self.bod_configurations[pos][1],
                        unit=self.bod_configurations[pos][0]))
                    bod_output = DeviceCommonFunctions().check_error_message(BOD, bod_reading)
                    if None not in bod_output.values():
                        return bod_output
            except Exception as ex:
                print(ex)

    class TemperatureSensor(object):
        """
        This class consist of functions which initilize the temperature_configurations and
        get the readings from Temperature Sensor.
        """

        def __init__(self):
            self.temperature_configurations = [[100, 9729, 10]]
            self.temperature_data_position = [0, 1]

        def get_temperature_reading(self):
            try:
                for pos in range(len(self.temperature_configurations)):
                    temperature_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.temperature_configurations[pos][2],
                        address=self.temperature_configurations[pos][1],
                        unit=self.temperature_configurations[pos][0]))
                    temperature_output = DeviceCommonFunctions().check_error_message(
                        Temperature, temperature_reading)
                    if None not in temperature_output.values():
                        return temperature_output
            except Exception as ex:
                print(ex)

    class TSSSensor(object):
        """
        This class consist of functions which initilize the tss_configurations and get the readings from TSS Sensor.
        """

        def __init__(self):
            self.tss_configurations = [[100, 4608, 4]]
            self.tss_data_position = [0, 1]

        def get_tss_reading(self):
            try:
                for pos in range(len(self.tss_configurations)):
                    tss_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tss_configurations[pos][2],
                        address=self.tss_configurations[pos][1],
                        unit=self.tss_configurations[pos][0]))
                    tss_output = DeviceCommonFunctions().check_error_message(TSS, tss_reading)
                    if None not in tss_output.values():
                        return tss_output
            except Exception as ex:
                print(ex)

    class PhSensor(object):
        """
        This class consist of functions which initilize the ph_configurations and get the readings from PH Sensor.
        """

        def __init__(self):
            self.ph_configurations = [[110, 9729, 5]]
            self.ph_data_position = [2, 3]

        def get_ph_reading(self):
            try:
                for pos in range(len(self.ph_configurations)):
                    ph_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.ph_configurations[pos][2],
                        address=self.ph_configurations[pos][1],
                        unit=self.ph_configurations[pos][0]))
                    ph_output = DeviceCommonFunctions().check_error_message(PH, ph_reading)
                    if None not in ph_output.values():
                        return ph_output
            except Exception as ex:
                print(ex)

    class TDSSensor(object):
        """
        This class consist of functions which initilize the tds_configurations and get the readings from TDS Sensor.
        """

        def __init__(self):
            self.tds_configurations = [[120, 9729, 4]]
            self.tds_data_position = [2, 3]

        def get_tds_reading(self):
            try:
                for pos in range(len(self.tds_configurations)):
                    tds_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.tds_configurations[pos][2],
                        address=self.tds_configurations[pos][1],
                        unit=self.tds_configurations[pos][0]))
                    tds_output = DeviceCommonFunctions().check_error_message(TDS, tds_reading)
                    if None not in tds_output.values():
                        return tds_output
            except Exception as ex:
                print(ex)

    class ConductivitySensor(object):
        """
        This class consist of functions which initilize the Conductivity_configurations and
        get the readings from Conductivity Sensor.
        """

        def __init__(self):
            self.conductivity_configurations = [[120, 9729, 4]]
            self.conductivity_data_position = [0, 1]

        def get_conductivity_reading(self):
            try:
                for pos in range(len(self.conductivity_configurations)):
                    conductivity_reading = (DeviceCommunication.gateway_connect().read_holding_registers(
                        count=self.conductivity_configurations[pos][2],
                        address=self.conductivity_configurations[pos][1],
                        unit=self.conductivity_configurations[pos][0]))
                    conductivity_output = DeviceCommonFunctions().check_error_message(
                        Conductivity, conductivity_reading)
                    if None not in conductivity_output.values():
                        return conductivity_output
            except Exception as ex:
                print(ex)


class DeviceDataLogging(object):
    """
    This class consist of functions to create json files for writing the sensor readings.
    """
    @classmethod
    def file_created(cls, files_pos):
        """
        Description: Return the Json file which generated.
        Input parameters: file position number
        Output type: Json file
        """
        try:
            base_dir = os.path.dirname(__file__)
            reading_dir = os.path.join(base_dir, 'Sensor_Readings')
            list_of_files = list(filter(lambda x: os.path.isfile(
                os.path.join(reading_dir, x)), os.listdir(reading_dir)))
            list_of_files = sorted(list_of_files, key=lambda x: os.path.getmtime(
                os.path.join(reading_dir, x)))
            return str(list_of_files[files_pos])
        except FileNotFoundError:
            Datalogs().logging_error(
                ValidationError["MKC2"], FileConfigurations["FunctionError"])
            return ValidationError["MKC2"]

    def sensor_readings_log(self, data):
        """
        Description: Open the last file generated,add sensor readings to that file.Once the file reaches 2000 lines,a
        new file is created.
        Input parameters: Sensor readings
        Output type: None
        """
        try:
            latest_file = self.file_created(-1)
            with open(r'Sensor_Readings/{}'.format(latest_file), 'r+') as file:
                file_data = json.load(file)
                if file_data:
                    last_number = int(list(file_data.keys())[-1])
                    data = {last_number + 1: data}
                else:
                    last_number = 0
                    data = {last_number + 1: data}
                if last_number == 2000:
                    last_number = 1
                file_data.update(data)
                if len(file_data.keys()) <= 2000:
                    file.truncate(0)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                else:
                    file_number = int(latest_file.split("_")[-1].split(".")[0])
                    with open(r'Sensor_Readings/Sensor_Readings_{}.json'.format(file_number + 1), "w") as file:
                        file.seek(0)
                        json.dump(data, file, indent=4)
        except FileNotFoundError:
            Datalogs().logging_error(
                ValidationError["MKC2"], FileConfigurations["FunctionError"])
            return ValidationError["MKC2"]
        except Exception:
            Datalogs().logging_error(
                ValidationError["MKC4"], FileConfigurations["FunctionError"])
            return ValidationError["MKC4"]

    @classmethod
    def get_sensors_readings(cls):
        result.update(DeviceCommonFunctions().get_local_time())
        result.update(EnergymeterSensor().get_energymeter_reading())
        result.update(STPSensor().CODSensor().get_cod_reading())
        result.update(STPSensor().BODSensor().get_bod_reading())
        result.update(STPSensor().TemperatureSensor().get_temperature_reading())
        result.update(STPSensor().PhSensor().get_ph_reading())
        result.update(STPSensor().TSSSensor().get_tss_reading())
        result.update(STPSensor().TDSSensor().get_tds_reading())
        result.update(STPSensor().ConductivitySensor().get_conductivity_reading())
        DeviceDataLogging().sensor_readings_log(result)
        print(result)
        return result


DeviceDataLogging().get_sensors_readings()
