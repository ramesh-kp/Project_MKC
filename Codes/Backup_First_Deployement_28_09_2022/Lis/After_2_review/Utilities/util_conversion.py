"""
This file consist of  common functions which are used in each sensor class
"""
import struct

from general_configurations import COMMAND_TYPE, ZEORES_FILL , DIGITS_2, JOIN_POSITION_2
from general_configurations import FORMAT_LENGTH, HEX_POSITION_0, REPLACE_VALUE

class Conversion(object):
    """
    This class consist of functions in relation with Stp Sensors and this functions are common
    functions which are used in each sensor class
    """
    @classmethod
    def little_to_big_endian(cls, input_str):
        """
        Description: Little Endian to Big Endian.Returns a new bytearray object in which every
        pair of neighbouring objects is reversed from the end, initialized from a string of
        hex numbers.
        Input Parameters: String containing hex numbers.
        Output Type: String

        """
        hex_string = bytearray.fromhex(input_str)
        hex_string.reverse()
        return ''.join(format(data, JOIN_POSITION_2 ) for data in hex_string).upper()

    def parse_rawdata(self, raw_data, data_pos_1, data_pos_2):
        """
        Description: Convert Raw Data to Real Value.Sensor reading at Array_Pos_1,Array_Pos_2 is
        convereted to hexadecimal format of length 4 the result is combined, converted to
        Bigindian Format, and then converted to decimal.
        Input Parameters: Readings from a sensor whose output will be in Little Indian format.
        Output Type: Decimal.

        """
        raw_data_hex_1 = hex(raw_data[data_pos_1]).replace(
            REPLACE_VALUE , '').zfill(ZEORES_FILL )
        raw_data_hex_2 = hex(raw_data[data_pos_2]).replace(
            REPLACE_VALUE, '').zfill(ZEORES_FILL )
        first_post_hex = self.little_to_big_endian(
            raw_data_hex_1 + raw_data_hex_2)
        reading = round(struct.unpack(
            '!f', bytes.fromhex(first_post_hex))[HEX_POSITION_0], DIGITS_2)
        return reading

class FormatMessage(object):
    """
    This class consist of function which send the readings to IOT in the mqtt message format
    """

    @classmethod
    def mqtt_message_format(cls, sensor_data, topic_name):
        """
        Description: Sensor data combined with Variable_Header to converts it to Mqtt message.
        Input parameters: Sensor readings
        Output type: String
        """
        data = str(sensor_data)
        mqtt_message = topic_name + \
            format(len(data), FORMAT_LENGTH ) + str(data)
        total_length = format(len(mqtt_message), FORMAT_LENGTH )
        final_message = COMMAND_TYPE + total_length + mqtt_message
        return final_message
