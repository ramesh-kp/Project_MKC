"""
This file consist of functions which establishes the connection with gateway client
and and get the local time
"""
from pymodbus.client.sync import ModbusTcpClient
from Utilities.util_error_mapping import Matching
from general_configurations import EMPTY_RETURN, GatewayConfiguration, GATEWAYIPADDRESS, GATEWAYPORT


class DeviceCommunication(object):
    """
    This class consist of functions which establishes the connection with gateway client
    and and get the local time
    """

    @classmethod
    def gateway_connect(cls):
        """
        """
        gateway_client = None
        gateway_client = ModbusTcpClient(
            GatewayConfiguration[GATEWAYIPADDRESS], GatewayConfiguration[GATEWAYPORT])
        gateway_client.connect()
        if gateway_client is not None:
            return gateway_client
        else:
            return Matching().error_mapping(EMPTY_RETURN)


