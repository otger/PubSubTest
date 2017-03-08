import time
import datetime


def get_utc_ts():
    now = datetime.datetime.utcnow()
    return time.mktime(now.timetuple()) + now.microsecond/1e6
