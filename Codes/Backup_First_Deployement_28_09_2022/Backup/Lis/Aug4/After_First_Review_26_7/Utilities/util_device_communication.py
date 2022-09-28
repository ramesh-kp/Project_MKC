from pymodbus.client.sync import ModbusTcpClient
from general_configurations import MKC26, GatewayConfiguration, GatewayIpAddress, GatewayPort, ValidationError


class DeviceCommunication(object):
    """
    This class consist of functions which establishes the connection with gateway client and and get the local time
    """

    @classmethod
    def gateway_connect(cls):
        gateway_client = None
        gateway_client = ModbusTcpClient(
            GatewayConfiguration[GatewayIpAddress], GatewayConfiguration[GatewayPort])
        gateway_client.connect()
        if gateway_client is not None:
            return gateway_client
        else:
            print(ValidationError[MKC26])
            return ValidationError[MKC26]

