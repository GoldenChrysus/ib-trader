from datetime import datetime
from dateutil import parser
from pytz import timezone
from time import sleep


def wait_until_time(time: str, tz: str) -> None:
    while True:
        tz_obj = timezone(tz)
        now = datetime.now(tz_obj)
        test = tz_obj.localize(parser.parse(time))

        if now >= test:
            return

        sleep(5 * 60)  # Sleep 5 minutes
