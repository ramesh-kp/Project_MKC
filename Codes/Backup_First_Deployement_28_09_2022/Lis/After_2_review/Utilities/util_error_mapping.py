'''
This file consist of function which map error with those in the Error_Messages.json
'''
import json
from general_configurations import FILEPATH, READ_MODE

class Matching(object):
    """
    This class consist of function which map error with those in the Error_Messages.json
    """

    def error_mapping(self, input_message):
        """
        Description: map error with those in the Error_Messages.json
        Input Parameters: Error messages
        Output Type: string
        """
        with open(FILEPATH, READ_MODE,encoding="utf-8") as file:
            error_message = json.load(file)
            return error_message[input_message]
