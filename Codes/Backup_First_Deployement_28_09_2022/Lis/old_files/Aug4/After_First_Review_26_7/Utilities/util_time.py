from datetime import datetime, timedelta

from general_configurations import MKC27, UTCLocalTime, ValidationError


class LocalTime:
    @classmethod
    def get_local_time(cls):
        current_time = str(datetime.utcnow() + timedelta(minutes=330))
        if current_time is  not None:
            time_stamp = {UTCLocalTime: current_time}
            return time_stamp
        else:
            print(ValidationError[MKC27])
            return ValidationError[MKC27]
