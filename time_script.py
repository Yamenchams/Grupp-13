import time

def get_current_time():
    # Get the current UTC time tuple
    utc_time = time.gmtime()
    
    # Assume CEST for now, which is UTC+2
    hour_offset = -11
    min_offset = 34

    # Calculate new hour with wrap-around at 24
    # Minutes wrap around at 60, also adjust hours if minutes exceed 60
    new_hour = (utc_time.tm_hour + hour_offset + (utc_time.tm_min + min_offset)) % 24
    new_minute = (utc_time.tm_min + min_offset) % 60

    # Ensure the hours, minutes, and seconds are two digits
    hour_str = str(new_hour) if new_hour > 9 else '0' + str(new_hour)
    min_str = str(new_minute) if new_minute > 9 else '0' + str(new_minute)
    sec_str = str(utc_time.tm_sec) if utc_time.tm_sec > 9 else '0' + str(utc_time.tm_sec)
    
    # Concatenate the time parts into a formatted time string
    formatted_time = hour_str + ':' + min_str + ':' + sec_str
    print(formatted_time)
    return formatted_time
