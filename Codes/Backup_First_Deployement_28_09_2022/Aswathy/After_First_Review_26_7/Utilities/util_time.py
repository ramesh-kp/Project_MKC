"""
This file consist of functions which deals with the local time.
"""
from datetime import datetime, timedelta

from general_configurations import MKC27, UTCLocalTime, ValidationError


class LocalTime(object):
    """
    This class consist of function which finds the local time.
    """
    @classmethod
    def get_local_time(cls):
        current_time = datetime.utcnow() + timedelta(minutes=330)
        local_time = str(current_time.strftime("%d/%m/%Y %H:%M:%S.%f"))
        if current_time is  not None:
            time_stamp = {UTCLocalTime: local_time}
            return time_stamp
        else:
            print(ValidationError[MKC27])
            return ValidationError[MKC27]
