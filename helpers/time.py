import datetime
import time
import pytz
from config.config import Config

config = Config()
config.parse()

DEFAULT_TIME_ZONE = "UTC"


def get_datetime(timestamp: int):
    timezone = config.get("timezone")
    return datetime.datetime.fromtimestamp(timestamp,
                                           tz=pytz.timezone(timezone if timezone is not None else DEFAULT_TIME_ZONE)
                                           )


def now_datetime():
    return get_datetime(time.time())
