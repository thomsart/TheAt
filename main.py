""" -*- coding: utf-8 -*-
"""

import tkinter as T

from alarm import *
from config import *
from events_commands import *
from scroll_year import *


##### TheAt config #####
TheAt = T.Tk()
TheAt.title('TheAt')
TheAt.minsize(280, 550)
TheAt.iconbitmap("static/assets/atom.ico")
TheAt.config(bg=ColorTheAt)

##### Header #####
header = T.Frame(TheAt)
header.grid()
welcome_tilte = T.Label(header, **FontParams, bg=ColorTheAt, text="Welcome in the TheAt !")
welcome_tilte.grid() # to display the title

##### Affichage de l'horloge #####
time = T.Label(TheAt, **FontParams, bg=ColorTheAt)
time.grid()

alarm = is_alarm_today(D.datetime.now())

##### Menu-Option #####
menu = T.Label(TheAt, **FontParams, bg=ColorTheAt, text="Menu")
menu.grid()

##### Body #####
body = T.Frame(TheAt)
body.grid()

##### Calandar #####
calandar = ScrollYear(body, D.datetime.now())
calandar.load_months()
calandar.mark_holydays()
calandar.mark_events()
calandar.mark_today()

##### Footer #####
footer = T.Frame(TheAt, bg=ColorTheAt)
footer.grid()
quit_button = T.Button(footer, **HomeButParams, text="Quit", command=TheAt.destroy)
quit_button.grid()

##### Refresh the application every 00h00 #####
def clock():
    """  """

    time.config(text=D.datetime.now().strftime("%H" + "h" + "%M" + ":" + "%S"))
    set_alarm(D.datetime.now(), alarm)

    if D.datetime.now().strftime("%H"+"%M"+"%S") == '000000':
        calandar.update_months(D.datetime.now())

    time.after(1000, clock)

clock()

##### Execute #####
if __name__ == '__main__':
    welcome_sound()
    TheAt.mainloop()
    goodbye_sound()
