import json
from general_configurations import filepath, read_mode

class Matching(object):

    def error_mapping(self, info):
        with open(filepath, read_mode) as file:
            error_message = json.load(file)
            return error_message[info]
