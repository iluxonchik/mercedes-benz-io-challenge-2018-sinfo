"""Date utility functions"""

import datetime

def isoformat_to_datetime(isoformat_str):
    dt_obj = datetime.datetime.strptime(isoformat_str, '%Y-%m-%dT%H:%M:%S')
    return dt_obj
