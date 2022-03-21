""" coding: utf-8
"""

import datetime as D
import tkinter as T
import winsound as w
import time as t

#######################################################################################################################
#######################################################################################################################
##### Colors ######

ColorTheAt = '#ffdb3b'
ColorText = '#5b5b5b'
ColorDay = '#ff0000'
ColorWE = '#e00000'
ColorHolyDay = '#ffdb3b'
ColorSchoolVacation = '#615cff'
ColorAnniversary = '#615cff'
ColorUniqueEvent = '#d035ff'
ColorCommandEvent = '#c3c7ff'

#######################################################################################################################
#######################################################################################################################
##### Widgets Parameters #####

FontParams = {
    "font": ("courier", 14),
    "fg": ColorText
}

HomeButParams = {
    'bg': ColorTheAt,
    'bd': 1,
    'relief': T.RIDGE
}
HomeButParams.update(FontParams)

DayButParams = {
    'bg': ColorDay,
    'bd': 1,
    'relief': T.RIDGE
}
DayButParams.update(FontParams)

WEButParams = {
    'bg': ColorWE,
    'bd': 1,
    'relief': T.RIDGE
}
WEButParams.update(FontParams)

EventButParams = {
    'bg': ColorCommandEvent,
    'bd': 1,
    'relief': T.RIDGE
}
EventButParams.update(FontParams)

EventTitreButParams = {
    'bg': ColorCommandEvent,
    'bd': 0,
    'relief': T.RIDGE
}
EventTitreButParams.update(FontParams)

days_letter_fr = ['L','M','M','J','V','S','D']
days_fr = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
days_letter_en = ['M','T','W','T','F','S','S']
days_en = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

#######################################################################################################################
#######################################################################################################################
###### Sounds #####

# def welcome_sound():
#     return winsound.PlaySound("sound.wav", winsound.SND_ASYNC)

# def beep_sound():
#     return winsound.MessageBeep()

def welcome_sound():
    """  """

    w.Beep(250, 200)
    w.Beep(300, 200)
    w.Beep(320, 200)
    w.Beep(350, 500)


def goodbye_sound():
    """  """

    w.Beep(350, 500)
    w.Beep(320, 200)
    w.Beep(300, 200)
    w.Beep(250, 200)


def alarm_sound():
    """  """

    w.Beep(3000, 30)
    w.Beep(3000, 30)
    w.Beep(3000, 30)

#######################################################################################################################
#######################################################################################################################
###### Dates ######

def reverse_date(str_date: str):
    """ This methode just reverse the date for the reading. """

    return str_date[8:10] + "/" + str_date[5:7] + "/" + str_date[:4]

def create_rolling_year(date: D.datetime.now()):
    """ On base of the date of today this method generates the twelve next months. """

    twelve_months = [date]
    year = date.year
    month = date.month

    for _ in range(0,11):
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        twelve_months.append(date.replace(year=year, month=month, day=1))

    return twelve_months
