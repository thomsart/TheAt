""" coding: utf-8
"""

import json as J
import tkinter as T

from config import *


def load_json(file: str):
    """  """

    try :
        json_file = open('events/' + file + '.json')
    except FileNotFoundError:
        with open('events/' + file + '.json', "w") as new_file:
            J.dump({}, new_file)
        json_file = open('events/' + file + '.json')

    copy = {}
    json = json_file.read()
    data = J.loads(json)
    copy.update(data)

    return copy


def overwrite_json(file: str, new_version: dict) -> bool:
    """  """

    try:
        with open('events/' + file + '.json', 'w') as new:
            J.dump(new_version, new)

        return True

    except:
        return False

#######################################################################################################################
#######################################################################################################################

def return_event_from_json(file: str, str_date: str) -> list:
    """ Methode use to return an event from json for a given date. """

    return_events = []
    with open('events/' + file + '.json', 'r') as _file:
                open_file = dict(J.load(_file))

    for month_day, contents in open_file.items():
        if month_day == str_date:
            for content in contents:
                return_events.append(content)

    return return_events

def is_events(str_date: str) -> list:
        """  """

        saved_events = []
        # first we check if there no every-year events for this date
        try:
            events = return_event_from_json('every_years', str_date[5:])
            # we check if the event is not a sequential event and occures this year or not
            for event in events:
                if event['start'] != None:
                    if int(str_date[:4]) in range(event['start'], 2100, event['step']):
                        continue
                    else:
                        events.remove(event)

            saved_events.extend(events)

        except Exception:
            try:
                saved_events.extend(return_event_from_json(str_date[:4], str_date[5:]))

                return saved_events

            except Exception:
                return False

        # then we check if there no unique events for this date
        try:
            saved_events.extend(return_event_from_json(str_date[:4], str_date[5:]))

        except Exception:
            if saved_events == []:
                return False

        return saved_events

#######################################################################################################################
#######################################################################################################################

def save_date_event(str_date: str, all_years: T.IntVar, freq: T.IntVar, start_year: T.StringVar, title: T.StringVar,
               alarm_range: list) -> bool:
    """ Create the json in function of datas """

    get_title = title.get()
    check_title = get_title.split()

    if check_title != []:
        ##### every years ? ######
        all_years = all_years.get()
        ##### every ? years ######
        freq = freq.get()
        if freq < 2 :
            freq = None
        ##### from ? year ######
        try:
            start_year = int(start_year.get())
            if start_year < 1900 or start_year > 2100:
                start_year = None
        except:
            start_year = None
        ##### title of the event ######
        set_title = ""
        iter = 0
        for caracter in get_title:
            iter += 1
            if caracter == " ":
                set_title = set_title + " "
                iter = 0
            elif caracter != " " and iter == 18:
                set_title = set_title + "- "
                iter = 0
            else:
                set_title = set_title + caracter
        set_title = set_title[:51]
        ##### alarm settings ? ######
        alarm = [alarm_range[0],alarm_range[-1]]
        alarm = sorted(alarm)

        ######################################################
        ######################################################

        if all_years:
            # we do a every years event
            copy = load_json('every_years')
            send = {}
            send.update(copy)

            for key, value in copy.items():
                if key == str_date[5:]:
                    send[str_date[5:]].append({"start": None, "step": None, "alarm": alarm, "?": set_title})

            send[str_date[5:]] = [{"start": None, "step": None, "alarm": alarm, "?": set_title}]
            send.update(copy)

            overwrite_json('every_years', send)

        else:
            # we do a every years event with freq step since start_year
            if freq != None and start_year != None:
                copy = load_json('every_years')
                send = {}
                send.update(copy)

                for key, value in copy.items():
                    if key == str_date[5:]:
                        send[str_date[5:]].append({"start": start_year, "step": freq, "alarm": alarm, "?": set_title})

                send[str_date[5:]] = [{"start": start_year, "step": freq, "alarm": alarm, "?": set_title}]
                send.update(copy)

                overwrite_json('every_years', send)

            else:
                # we do a single event for the current year
                copy = load_json(str_date[:4])
                send = {}
                send.update(copy)

                for key, value in copy.items():
                    if key == str_date[5:]:
                        send[str_date[5:]].append({"alarm": alarm, "?": set_title})

                send[str_date[5:]] = [{"alarm": alarm, "?": set_title}]
                send.update(copy)

                overwrite_json(str_date[:4], send)
    else:
        return False


def save_day_event():
    """  """
    pass

#######################################################################################################################
#######################################################################################################################

def delete_event(str_date: str, event_title: str):
    """  """

    files = ['every_years', str_date[:4]]

    for file in files:
        try:
            copy = load_json(file)
            send = {}
            send.update(copy)
            if copy.get(str_date[5:]):
                for event in copy[str_date[5:]]:
                    if event['?'] == event_title:
                        copy[str_date[5:]].remove(event)
            else:
                continue
            # we clean the json if it contains date with no events -> []
            for key, value in copy.items():
                if len(value) == 0:
                    del send[key]
                else:
                    continue
            # finally we overwrite the json_file with the new datas
            overwrite_json(file, send)

        except FileNotFoundError:
            continue
