import time

def get_current_time():
    # Get the current UTC time tuple
    utc_time = time.gmtime()
    
    # Assume CEST for now, which is typically UTC+2
    hour_offset = 13  # Adjust to UTC+2 for CEST
    min_offset = -26   # No minute offset necessary unless needed

    # Calculate new hour with wrap-around at 24
    # Minutes wrap around at 60, also adjust hours if minutes exceed 60
    new_hour = (utc_time.tm_hour + hour_offset) % 24
    new_minute = (utc_time.tm_min + min_offset) % 60

    # Ensure the hours, minutes, and seconds are two digits
    hour_str = "{:02}".format(new_hour)
    min_str = "{:02}".format(new_minute)
    sec_str = "{:02}".format(utc_time.tm_sec)
    
    # Concatenate the time parts into a formatted time string
    formatted_time = hour_str + ':' + min_str + ':' + sec_str
    return formatted_time

