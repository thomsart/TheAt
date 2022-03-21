""" coding: utf-8
"""

from typing import Optional
from config import *
from events_commands import is_events


def is_alarm_today(date: D.datetime.now()):
    """  """

    date = str(date)[:10]
    events = is_events(date)

    if events:
        hours = [event['alarm'] for event in events]
        start_stop = []
        for hour_set in hours:
            start_stop.append(hour_set[0])
            start_stop.append(hour_set[1])
        start_stop = sorted(start_stop)

        return [start_stop[0], start_stop[-1]]

    else:
        return None


def set_alarm(time: D.datetime.now(), start_stop: Optional[list]=None):
    """  """

    if start_stop:
        hour = int(time.strftime("%H"))
        minute = int(time.strftime("%M"))
        second = int(time.strftime("%S"))

        if start_stop[0] <= hour <= start_stop[1] and minute in (0, 30) and second <= 10:
            alarm_sound()

