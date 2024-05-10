import time


def get_current_time():

    utc_time = time.gmtime()

    hour_offset = 13
    min_offset = -26

    new_hour = (utc_time.tm_hour + hour_offset) % 24
    new_minute = (utc_time.tm_min + min_offset) % 60

    hour_str = "{:02}".format(new_hour)
    min_str = "{:02}".format(new_minute)
    sec_str = "{:02}".format(utc_time.tm_sec)

    formatted_time = hour_str + ':' + min_str + ':' + sec_str
    return formatted_time

