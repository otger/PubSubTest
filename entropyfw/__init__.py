import time
import datetime

from entropyfw.module.module import Module
from entropyfw.module.actionmanager import Action
from entropyfw.module.eventcallbacks import Callback

def get_utc_ts():
    now = datetime.datetime.utcnow()
    return time.mktime(now.timetuple()) + now.microsecond/1e6
