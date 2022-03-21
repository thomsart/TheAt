""" -*- coding: utf-8 -*-

"""

from typing import Optional
import calendar as C
import tkinter as T

from config import *
from events_commands import *


class ScrollYear(T.Tk):

    def __init__(self, parent: T.Frame, datetime: D.datetime):

        self.date = datetime
        self.months = months = T.Frame(parent, bg=ColorTheAt)
        months.grid(sticky='news')
        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = frame_canvas = T.Frame(self.months)
        frame_canvas.grid(row=1, column=0, sticky='nw', padx=2, ipady=150)
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 7-by-7 buttons resizing later
        frame_canvas.grid_propagate(False)
        # Add a canvas in that frame
        self.canvas = canvas = T.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky="news")
        # Link a scrollbar to the canvas
        self.vsb = vsb = T.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        # Create a frame to contain the buttons
        self.frame_buttons = frame_buttons = T.Frame(canvas)
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
        self.rows = [0,1,2,3,4,5,6,7,8]
        self.columns = 7
        self.buttons = [[T.Button() for c in range(self.columns)] for i in range(0, 109)]
        self.today = T.PhotoImage(file="static/image/today/" + str(self.date)[8:10] + ".png")
        self.anniversary = T.PhotoImage(file="static/image/anniversary.png")
        self.unique_event = T.PhotoImage(file="static/image/unique_event.png")

#######################################################################################################################
#######################################################################################################################

    def show_date_events(self, date: str):
        """ This method is use to display and create events on this date """

        # we check if first the file exist or if an event exist on this date
        events = is_events(date)

        if events:
            event_lf = T.LabelFrame(self.canvas, **EventButParams, text='    ' + 'Le ' + reverse_date(date) + '    ')
            event_lf.grid(row= 2, padx=5, pady=5)
            event_lf.after(3000, event_lf.destroy)

            row = 0
            T.Label(event_lf, bd=0, bg=ColorCommandEvent, **FontParams,
                    text='----------------------').grid(row=row, rowspan=1)

            for event in events:
                # now for each event we take care of number of letters to not overflow 20
                event_words_list = event['?'].split()
                count = 0
                index = -1
                row += 1
                rowspan = 1

                for word in event_words_list:
                    count += 1 # for the space or dot above each word
                    index += 1
                    for letter in word:
                        count += 1

                    if count > 19:
                        event_words_list.insert(index,'\n')
                        count = 0
                        row += 1
                        rowspan += 1

                text = " ".join(event_words_list)

                show = T.Button(event_lf, **EventTitreButParams, text='.' + text, justify='left', width=19,
                            command=lambda x=date, y=event['?']:[self.ask_to_delete(x, y), event_lf.destroy()])
                show.grid(row=row, rowspan=rowspan)
                row += 1

            row += 3
            T.Label(event_lf, bd=0, bg=ColorCommandEvent, **FontParams,
                    text='----------------------').grid(row=row, rowspan=1)

            row += 1
            new_event = T.Button(event_lf, **EventButParams, text='Nouveau',
                                command=lambda x=date:[self.create_year_event(x), event_lf.destroy()])
            new_event.grid(row=row)

        # and if there no evens on this day we directly display the create event window
        else:
            self.create_year_event(date)


    def show_day_events(self, day_letter):
        """ This method is use to display and create events on this day. """

        event_lf = T.LabelFrame(self.canvas, **EventButParams, text=' Tout les ' + days_fr[day_letter] + 's ')
        event_lf.grid(row= 2, padx=5, pady=50)
        event_lf.after(3000, event_lf.destroy)

        T.Label(event_lf, bd=0, bg=ColorCommandEvent, **FontParams,
                    text='----------------------').grid(row=3, rowspan=1)

        T.Label(event_lf, bd=0, bg=ColorCommandEvent, **FontParams,
                    text='----------------------').grid(row=6, rowspan=1)

        new_event = T.Button(event_lf, **EventButParams, text='nouveau')
        new_event.grid(row=7)


#######################################################################################################################
#######################################################################################################################


    def colorize_button(self, date: str, color: str):
        """ This method allows to colorize a button if its name equal a date. """

        for day_button in self.frame_buttons.winfo_children():
            if day_button.winfo_name()[5:10] == date or day_button.winfo_name()[:10] == date:
                day_button.config(image="", bg=color)


    def colorize_text(self, date: str, color: str):
        """ This method allows to colorize the text of a button if its name equal a date. """

        for day_button in self.frame_buttons.winfo_children():
            if day_button.winfo_name()[5:10] == date:
                day_button.config(image="", fg=color)


    def mark_anniversary(self, date: str):
        """ This method allows to add an anniversary.png for a better visibility. """

        for day_button in self.frame_buttons.winfo_children():
            if day_button.winfo_name()[5:10] == date:
                day_button.config(image=self.anniversary)


    def mark_unique_event(self, date: str):
        """ This method allows to add an unique_event.png for a better visibility. """

        for day_button in self.frame_buttons.winfo_children():
            if day_button.winfo_name()[:10] == date:
                day_button.config(image=self.unique_event)


    def mark_holydays(self):
        """ This method is used to mark all holydays and school vacations """

        with open('events/holydays.json', 'r') as _particular_days:
                    particular_days = dict(J.load(_particular_days))

        for key, value in particular_days.items():
            if value == "holyday":
                self.colorize_text(key, ColorSchoolVacation)
            else:
                self.colorize_text(key, ColorHolyDay)


    def mark_events(self, date: Optional[str]=None):
        """ This Method is use to colorize all event trought the current year. """

        if date:
            try:
                with open('events/every_years.json', 'r') as every_year:
                    every_year = dict(J.load(every_year))

                if every_year.get(date[5:]):
                    if is_events(date):
                        self.mark_anniversary(date[5:])

                else:
                    self.colorize_button(date, ColorDay)

                    try:
                        with open('events/' + date[:4] + '.json', 'r') as curent_year:
                            curent_year = dict(J.load(curent_year))

                        if curent_year.get(date[5:]):
                            self.mark_unique_event(date)
                        else:
                            print('y a plus dans ' + date[:4])
                            self.colorize_button(date, ColorDay)

                    except FileNotFoundError:
                        print("No " + date[:4] + ".json exist")

            except FileNotFoundError:
                print("No every_years.json exist")

        # and if there is no date we parse all files
        else:
            this_year = str(self.date)
            next_year = str(self.date.replace(year=self.date.year+1))

            try:
                with open('events/every_years.json', 'r') as every_year:
                    every_year = dict(J.load(every_year))

                for month_day in every_year.keys():
                    if is_events(this_year[:5]+month_day):
                        self.mark_anniversary(month_day)
                    elif is_events(next_year[:5]+month_day):
                        self.mark_anniversary(month_day)

            except FileNotFoundError:
                print("No every_years.json exist")

            try:
                with open('events/' + this_year[:4] + '.json', 'r') as curent_year:
                    curent_year = dict(J.load(curent_year))

                for month_day in curent_year.keys():
                    self.mark_unique_event(this_year[:5] + month_day)

            except FileNotFoundError:
                print("No " + this_year[:4] + ".json exist")

            try:
                with open('events/' + next_year[:4] + '.json', 'r') as futur_year:
                    futur_year = dict(J.load(futur_year))

                for month_day in futur_year.keys():
                    self.mark_unique_event(next_year[:5] + month_day)

            except FileNotFoundError:
                print("No " + next_year[:4] + ".json exist")


    def mark_today(self):
        """ This method is used to just mark today. """

        for day_button in self.frame_buttons.winfo_children():
            if day_button.winfo_name()[:10] == str(self.date)[:10]:
                day_button.config(image=self.today)


#######################################################################################################################
#######################################################################################################################


    def create_year_event(self, date: str):
        """ This method is use to create event on this date. """

        event = T.LabelFrame(self.canvas, **EventButParams, text='   ' + 'Le ' + reverse_date(date) + '   ')
        event.grid(row=1, padx=10, pady=50)
        event.after(60000, event.destroy)

        T.Label(event, bg=ColorCommandEvent).grid(row=0)

        state_all_years = T.IntVar()
        state_all_years.set(0)
        T.Checkbutton(event, **FontParams, bg=ColorCommandEvent, relief=T.RIDGE, text='Tout les ans',
                    variable=state_all_years).grid(row=1, columnspan=6)

        T.Label(event, **FontParams, bg=ColorCommandEvent, text="Ou tout les").grid(row=2, column=0, columnspan=4)
        freq = T.IntVar()
        T.Entry(event, **FontParams, bg=ColorCommandEvent, width=2, textvariable=freq).grid(row=2, column=5, columnspan=1)
        T.Label(event, **FontParams, bg=ColorCommandEvent, text="ans").grid(row=2, column=6, columnspan=2)

        T.Label(event, **FontParams, bg=ColorCommandEvent, text="depuis l'année").grid(row=3, columnspan=5)
        start = T.StringVar()
        T.Entry(event, **FontParams, bg=ColorCommandEvent, width=4, textvariable=start).grid(row=3, column=5, columnspan=4)

        T.Label(event, bg=ColorCommandEvent).grid(row=4)

        T.Label(event, **FontParams, bg=ColorCommandEvent, text="Titre:").grid(row=5, columnspan=8)

        title = T.StringVar()
        T.Entry(event, **FontParams, bg=ColorCommandEvent, width=20, textvariable=title).grid(row=6, columnspan=10)

        T.Label(event, bg=ColorCommandEvent).grid(row=7)

        T.Label(event, **FontParams, bg=ColorCommandEvent, text="Alarm:").grid(row=8, columnspan=8)

        hour_range = T.StringVar(value=[str(nb) + 'h' for nb in range(0, 24)])
        alarm_range = [8,18]

        T.Label(event, **FontParams, bg=ColorCommandEvent, text="de").grid(row=9, column=2)

        alarm_start = T.Listbox(event, **FontParams, selectmode='single', height=5, width=4,
                                listvariable=hour_range)
        alarm_start.grid(row=10, column=2)
        
        T.Label(event, **FontParams, bg=ColorCommandEvent, text="à").grid(row=9, column=5)

        alarm_end = T.Listbox(event, **FontParams, selectmode='single', height=5, width=4,
                              listvariable=hour_range)
        alarm_end.grid(row=10, column=5)

        def chosen_hour(event):
            """ Get selected indices """

            try:
                alarm_start_hour = alarm_start.curselection()
                alarm_range.insert(0, alarm_start_hour[0])
            except IndexError:
                alarm_end_hour = alarm_end.curselection()
                alarm_range.append(alarm_end_hour[0])

        alarm_start.bind('<<ListboxSelect>>', chosen_hour)
        alarm_end.bind('<<ListboxSelect>>', chosen_hour)

        T.Label(event, bg=ColorCommandEvent).grid(row=11)

        T.Button(event, **EventButParams, text="Save", command=lambda
            a=state_all_years, b=freq, c=start, d=title, e=alarm_range:
            [save_date_event(date, a,b,c,d,e), self.mark_events(date), event.destroy()]).grid(row=12, column=1, columnspan=2)
        T.Button(event, **EventButParams, text="Quit", command=event.destroy).grid(row=12, column=4, columnspan=2)


    def ask_to_delete(self, date: str, event_title: str):
        """ This method display the window in which we ask the user if he want to delete this event. """

        event_lf = T.LabelFrame(self.canvas, **EventButParams, text=event_title[:10])
        event_lf.grid(row= 2, padx=20, pady=50)
        event_lf.after(3000, event_lf.destroy)

        T.Label(event_lf, **EventTitreButParams, text='Supprimer cet évènement ?').grid(row=1)

        T.Button(event_lf, **EventButParams, text='Oui', command=lambda x=date, y=event_title:
                [delete_event(x, y), self.mark_events(x), event_lf.destroy()]).grid(row=3)

#######################################################################################################################
#######################################################################################################################


    def load_months(self):
        """ this method just load all 12 next months from the current one. """

        years_months = create_rolling_year(self.date)
        for date in years_months:
            year = str(date.year)
            days_in_this_month = C.monthrange(year=date.year, month=date.month)
            days = [day + 1 for day in range(days_in_this_month[1])]
            month_year = [date.strftime('%B')[0], date.strftime('%B')[1].capitalize(),
                          date.strftime('%B')[2].capitalize(), year[0], year[1], year[2], year[3]]

            def create_day_button(params, day_in_week):
                """ the goal of this method is to name each button with date """

                return T.Button(self.frame_buttons, params, text= str(days[0]),
                                name=str(D.date(year=date.year, month=date.month, day=days[0]))+"-"+str(day_in_week),
                                command=lambda x=str(D.date(year=date.year, month=date.month, day=days[0])):
                                self.show_date_events(x))

            for r in self.rows:
                # LINE 01 -> a line to do a space for the esthetic
                if r in range(0,108,9):
                    for c in range(self.columns):
                        self.buttons[r][c] = T.Label(self.frame_buttons, bg=ColorTheAt, text="   ")
                        self.buttons[r][c].grid(row=r, column=c, sticky='news')
                # LINE 02 -> the line with the month and the year in letters
                elif r in range(1,109,9):
                    for c in range(self.columns):
                        self.buttons[r][c] = T.Label(
                            self.frame_buttons, **FontParams, bg=ColorTheAt, text=month_year[c])
                        self.buttons[r][c].grid(row=r, column=c, sticky='news')
                # LINE 03 -> line with the first letter of each day
                elif r in range(2,110,9):
                    for c in range(self.columns):
                        self.buttons[r][c] = T.Button(
                                            self.frame_buttons, **FontParams, bd= 1, relief=T.RIDGE, bg="white",
                                            text=days_letter_fr[c],
                                            command=lambda x=c:
                                                self.show_day_events(x))
                        self.buttons[r][c].grid(row=r, column=c, sticky='news')
                # LINE 04 -> all lines for the days
                elif r in range(3,111,9):
                    for c in range(self.columns):
                        if c < days_in_this_month[0]:
                            self.buttons[r][c] = T.Label(self.frame_buttons, bg=ColorTheAt, text="   ")
                        elif c == days_in_this_month[0]:
                            if c >= 5:
                                self.buttons[r][c] = create_day_button(WEButParams, c)
                            else:
                                self.buttons[r][c] = create_day_button(DayButParams, c)
                            del days[0]
                        else:
                            if c >= 5:
                                self.buttons[r][c] = create_day_button(WEButParams, c)
                            else:
                                self.buttons[r][c] = create_day_button(DayButParams, c)
                            del days[0]
                        self.buttons[r][c].grid(row=r, column=c, sticky='news')
                # LINE 05 06 07 08 09
                else:
                    for c in range(self.columns):
                        try:
                            if c >= 5:
                                self.buttons[r][c] = create_day_button(WEButParams, c)
                            else:
                                self.buttons[r][c] = create_day_button(DayButParams, c)
                            self.buttons[r][c].grid(row=r, column=c, sticky='news')
                            del days[0]
                        except IndexError:
                                self.buttons[r][c] = T.Label(self.frame_buttons, bg=ColorTheAt, text="   ")
                        self.buttons[r][c].grid(row=r, column=c, sticky='news')

            self.rows = [row + 9 for row in self.rows]

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()
        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first7columns_width = sum([self.buttons[0][c].winfo_width() for c in range(self.columns)])
        first7rows_height = sum([self.buttons[r][0].winfo_height() for r in range(self.columns)])
        self.frame_canvas.config(width=first7columns_width + self.vsb.winfo_width(), height=first7rows_height)
        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def update_months(self, datetime: D.datetime):
        """  """

        for day_button in self.frame_buttons.winfo_children():
            day_button.grid_forget()

        self.rows = [0,1,2,3,4,5,6,7,8]
        self.date = datetime

        self.load_months()
        self.mark_holydays()
        self.mark_events()
        self.mark_today()
