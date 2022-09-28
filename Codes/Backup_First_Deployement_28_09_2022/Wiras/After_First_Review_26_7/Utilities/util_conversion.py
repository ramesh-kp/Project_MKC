"""
This file consist of  common functions which are used in each sensor class
"""
import struct

from general_configurations import Command_Type, zeores_fill, digits_2, join_position_2, replace_value, hex_position_0
from general_configurations import format_length

class Conversion(object):
    """
    This class consist of functions in relation with Stp Sensors and this functions are common functions which are used
    in each sensor class
    """
    @classmethod
    def little_to_big_endian(cls, input_str):
        hex_string = bytearray.fromhex(input_str)
        hex_string.reverse()
        return ''.join(format(data, join_position_2) for data in hex_string).upper()

    def parse_rawdata(self, raw_data, data_pos_1, data_pos_2):
        raw_data_hex_1 = hex(raw_data[data_pos_1]).replace(
            replace_value, '').zfill(zeores_fill)
        raw_data_hex_2 = hex(raw_data[data_pos_2]).replace(
            replace_value, '').zfill(zeores_fill)
        first_post_hex = self.little_to_big_endian(
            raw_data_hex_1 + raw_data_hex_2)
        reading = round(struct.unpack(
            '!f', bytes.fromhex(first_post_hex))[hex_position_0], digits_2)
        return reading

class FormatMessage(object):

    @classmethod
    def mqtt_message_format(cls, sensor_data, topic_name):
        """
        Description: Sensor data combined with Variable_Header to converts it to Mqtt message.
        Input parameters: Sensor readings
        Output type: String
        """
        data = str(sensor_data)
        mqtt_message = topic_name + \
            format(len(data), format_length) + str(data)
        total_length = format(len(mqtt_message), format_length)
        final_message = Command_Type + total_length + mqtt_message
        return final_message

