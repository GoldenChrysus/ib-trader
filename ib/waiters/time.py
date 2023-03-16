from datetime import datetime, timedelta
from dateutil import parser
from pytz import timezone
from time import sleep


def wait_until_time(time: str, tz: str, include_weekends=False) -> None:
    tz_obj = timezone(tz)
    test = tz_obj.localize(parser.parse(time))

    if not include_weekends:
        test_weekday = test.weekday()

        if test_weekday in {5, 6}:
            days_to_add = 7 - test_weekday
            test = test + timedelta(days=days_to_add)

    print('waiting until %s' % (test))

    while True:
        now = datetime.now(tz_obj)

        if now >= test:
            return

        sleep(5 * 60)  # Sleep 5 minutes
