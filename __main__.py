import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from Scraper import update_calendar
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.graphics import Canvas, Color,Rectangle
from kivy.core.window import Window
from Calendar import Event, initialize, find_today_date, monthConverter, build_calendar, find_current_week_dates

record = open("UpdateRecord.txt", "r")
record_valuee = record.read()
record.close()
event_list = initialize()

today_day = find_today_date()[0]
today_month = find_today_date()[1]
today_year = find_today_date()[2]

current_day = today_day
current_month = today_month
current_year = today_year



class WindowManager(ScreenManager):
    pass


class MainMenu(Screen):

    record_value = StringProperty(None)
    record_value = record_valuee


class ScrapeMenu(Screen):
    starting_date = ObjectProperty(None)
    ending_date = ObjectProperty(None)

    def update_btn(self):
        update_calendar(self.starting_date.text, self.ending_date.text)


month_converter = {
    '1': 'Jan',
    '2': 'Feb',
    '3': 'Mar',
    '4': 'Apr',
    '5': 'May',
    '6': 'Jun',
    '7': 'Jul',
    '8': 'Aug',
    '9': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'

}




class DateSelect(FloatLayout):

    def confirm_change_current_date(self, instance, day):
        if day != '':
            global current_year, current_month, current_day
            current_year = instance.current_select_year
            current_month = instance.current_select_month
            current_day = day
        print(current_day,current_month,current_year)

        self.clear_widgets()
        self.update_calendar_display()
        self.window.update_event()
    def change_year_month(self, instance, year, month):
        if year == 2:
            self.yr = self.current_select_year
            self.yr2 = int(self.yr) + 1
        if year == 1:
            self.yr = self.current_select_year
            self.yr2 = int(self.yr) - 1

        if month == 2:
            self.m = self.current_select_month
            month_no= monthConverter[self.m]
            month_no+=1
            if month_no == 13:
                month_no = 1
            self.m2= month_converter[str(month_no)]
        if month == 1:
            self.m = self.current_select_month
            month_no= monthConverter[self.m]
            month_no-=1
            if month_no == 0:
                month_no = 12

            self.m2= month_converter[str(month_no)]

        if year!=0:
            self.current_select_year = str(self.yr2)
        if month!=0:
            self.current_select_month = self.m2
        self.clear_widgets()
        self.update_calendar_display()


    def update_calendar_display(self):
        # select year month row

        self.left_year_btn = Button(text="<", size_hint=self.btn_size, pos_hint={"y": 0.85, "x": 0.1},
                                    background_color=(0, 0, 0, 0), font_size=20)
        self.left_year_btn.bind(on_release=lambda x: self.change_year_month(self,1,0))
        self.year_label = Label(text=self.current_select_year, size_hint=(0.2, 0.1), pos_hint={"y": 0.85, "x": 0.2},
                                font_size=20)
        self.right_year_btn = Button(text=">", size_hint=self.btn_size, pos_hint={"y": 0.85, "x": 0.4},
                                     background_color=(0, 0, 0, 0), font_size=20)
        self.right_year_btn.bind(on_release=lambda x: self.change_year_month(self,2,0))
        self.add_widget(self.left_year_btn)
        self.add_widget(self.year_label)
        self.add_widget(self.right_year_btn)
        self.left_month_btn = Button(text="<", size_hint=self.btn_size, pos_hint={"y": 0.85, "x": 0.6},
                                background_color=(0, 0, 0, 0), font_size=20)
        self.left_month_btn.bind(on_release=lambda x: self.change_year_month(self, 0, 1))
        self.add_widget(
            Label(text=self.current_select_month, size_hint=(0.1, 0.1), pos_hint={"y": 0.85, "x": 0.7}, font_size=20))
        self.right_month_btn = Button(text=">", size_hint=self.btn_size, pos_hint={"y": 0.85, "x": 0.8},
                                 background_color=(0, 0, 0, 0), font_size=20)
        self.right_month_btn.bind(on_release=lambda x: self.change_year_month(self, 0, 2))
        self.add_widget(self.left_month_btn)
        self.add_widget(self.right_month_btn)

        # select day grid
        weekday = ['S', 'M', 'T', 'W', 'T', 'F', 'S']

        for i in range(7):
            self.add_widget(
                Label(text=weekday[i], size_hint=(0.1, 0.1), pos_hint={"y": 0.7, "x": (0.3 / 8 * (i + 1) + i * 0.1)},
                      font_size=20))
        self.day_list = build_calendar(int(self.current_select_year), self.current_select_month)
        i=0
        day_btn=[]
        for y in range(5):
            for x in range(7):

                if self.day_list[i] == 0:
                    day_btn.append((Button(text='', size_hint=(0.1, 0.1),
                                     pos_hint={"y": 0.7 - (y + 1) * 0.1 - 0.1/6*(y+1), "x": (0.3 / 8 * (x + 1) + x * 0.1)}, font_size=20,
                                     background_color=(0,0,0,0))))
                else:
                    self.d=str(self.day_list[i])
                    if self.d==current_day and current_month==self.current_select_month:
                        bg_color = (1, 1, 0, 1)
                    else:
                        bg_color = (0, 0, 0, 0)
                    day_btn.append( Button(text=self.d, size_hint=(0.1, 0.1),
                                     pos_hint={"y": 0.7 - (y + 1) * 0.1- 0.1/6*(y+1), "x": (0.3 / 8 * (x + 1) + x * 0.1)}, font_size=20,
                                     background_color=bg_color))

                i+=1
        day_btn[0].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[0].text))
        self.add_widget(day_btn[0])
        day_btn[1].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[1].text))
        self.add_widget(day_btn[1])
        day_btn[2].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[2].text))
        self.add_widget(day_btn[2])
        day_btn[3].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[3].text))
        self.add_widget(day_btn[3])
        day_btn[4].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[4].text))
        self.add_widget(day_btn[4])
        day_btn[5].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[5].text))
        self.add_widget(day_btn[5])
        day_btn[6].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[6].text))
        self.add_widget(day_btn[6])
        day_btn[7].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[7].text))
        self.add_widget(day_btn[7])
        day_btn[8].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[8].text))
        self.add_widget(day_btn[8])
        day_btn[9].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[9].text))
        self.add_widget(day_btn[9])
        day_btn[10].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[10].text))
        self.add_widget(day_btn[10])
        day_btn[11].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[11].text))
        self.add_widget(day_btn[11])
        day_btn[12].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[12].text))
        self.add_widget(day_btn[12])
        day_btn[13].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[13].text))
        self.add_widget(day_btn[13])
        day_btn[14].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[14].text))
        self.add_widget(day_btn[14])
        day_btn[15].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[15].text))
        self.add_widget(day_btn[15])
        day_btn[16].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[16].text))
        self.add_widget(day_btn[16])
        day_btn[17].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[17].text))
        self.add_widget(day_btn[17])
        day_btn[18].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[18].text))
        self.add_widget(day_btn[18])
        day_btn[19].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[19].text))
        self.add_widget(day_btn[19])
        day_btn[20].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[20].text))
        self.add_widget(day_btn[20])
        day_btn[21].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[21].text))
        self.add_widget(day_btn[21])
        day_btn[22].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[22].text))
        self.add_widget(day_btn[22])
        day_btn[23].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[23].text))
        self.add_widget(day_btn[23])
        day_btn[24].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[24].text))
        self.add_widget(day_btn[24])
        day_btn[25].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[25].text))
        self.add_widget(day_btn[25])
        day_btn[26].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[26].text))
        self.add_widget(day_btn[26])
        day_btn[27].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[27].text))
        self.add_widget(day_btn[27])
        day_btn[28].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[28].text))
        self.add_widget(day_btn[28])
        day_btn[29].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[29].text))
        self.add_widget(day_btn[29])
        day_btn[30].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[30].text))
        self.add_widget(day_btn[30])
        day_btn[31].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[31].text))
        self.add_widget(day_btn[31])
        day_btn[32].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[32].text))
        self.add_widget(day_btn[32])
        day_btn[33].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[33].text))
        self.add_widget(day_btn[33])
        day_btn[34].bind(on_press=lambda x: self.confirm_change_current_date(self, day_btn[34].text))
        self.add_widget(day_btn[34])





    def __init__(self,window,**kwargs):
        self.btn_size = (0.1, 0.1)
        super(DateSelect, self).__init__(**kwargs)
        self.window = window
        self.current_select_year = current_year
        self.current_select_month = current_month
        self.current_select_day = current_day
        print(current_day,current_month,current_year)
        self.update_calendar_display()

#/////////////////////////////////////////////////////////////////////////////////////
class EventWeeklyLocalList:

    def __init__(self, weekday, number, name, date, time, for_mat, location, course):
        self.weekday = weekday
        self.number = number
        self.name = name
        self.date = date
        self.time = time
        self.for_mat = for_mat
        self.location = location
        self.course = course

class EventDetailPopup(FloatLayout):
    def __init__(self,name, date, time, for_mat, location, course, **kwargs):
        self.name = name
        self.date = date
        self.time = time
        self.for_mat = for_mat
        self.location = location
        self.course = course
        super(EventDetailPopup, self).__init__(**kwargs)
        self.add_widget(Label(text=self.name, size_hint=(0.75,0.1), pos_hint={"x":0.125,"y":0.775}))
        self.add_widget(Label(text=self.course, size_hint=(0.75, 0.1), pos_hint={"x": 0.125, "y": 0.675}))
        self.add_widget(Label(text=self.for_mat, size_hint=(0.75, 0.1), pos_hint={"x": 0.125, "y": 0.575}))
        self.add_widget(Label(text=self.date, size_hint=(0.75, 0.1), pos_hint={"x": 0.125, "y": 0.475}))
        self.add_widget(Label(text=self.time, size_hint=(0.75, 0.1), pos_hint={"x": 0.125, "y": 0.375}))
        self.add_widget(Label(text=self.location, size_hint=(0.75, 0.1), pos_hint={"x": 0.125, "y": 0.275}))

class EventView(FloatLayout):


    def event_detail(self, selected_weekday, selected_number):
        self.selected_weekday = selected_weekday
        self.selected_number = selected_number
        print('selected weekday:'+ str(self.selected_weekday)+' selected numbr: '+str(self.selected_number))
        for event in self.local_event_week_list:
            if event.weekday == self.selected_weekday and event.number == self.selected_number:
                detail_window = EventDetailPopup(event.name,event.date, event.time, event.for_mat, event.course,event.location)
                popup_window = Popup(title="Detail", content=detail_window, size_hint=(0.75, 0.75))
                popup_window.open()
                self.relative_x = 0
                self.relative_y = 0
                break

    def on_touch_up(self, touch):
        self.selected_weekday = 0
        self.selected_number = 0
        self.relative_x = touch.pos[0]/Window.width
        self.relative_y = touch.pos[1] / Window.height
        print(self.relative_x,self.relative_y)
        for i in range(1,8):
            if 0.12*(i+1)+ 0.04 / 9 * (i + 2)> self.relative_x > 0.12*i+ 0.04 / 9 * (i + 1):
                self.selected_weekday = i
                break
        for i in range(1,7):
            if 0.8-(i-1)*0.13> self.relative_y > 0.8-i*0.13:
                self.selected_number = i
                break
        self.event_detail(self.selected_weekday, self.selected_number)



    def __init__(self, **kwargs):
        self.local_event_week_list = []
        self.selected_weekday = 0
        self.selected_number = 0
        weekday = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        global current_year, current_month, current_day
        self.day_dates = find_current_week_dates(int(current_year),current_month,int(current_day))
        super(EventView, self).__init__(**kwargs)
        for i in range(1,8):
            if today_day==str(self.day_dates[i-1].day) and today_month==month_converter[str(self.day_dates[i-1].month)] and today_year ==str(self.day_dates[i-1].year):

                self.add_widget(Label(text=str(self.day_dates[i-1].day) +'/'+str(self.day_dates[i-1].month)+'\n    '+ weekday[i-1], font_size = '20', size_hint=(0.12,0.16), color=(1,0,0,1), pos_hint={"x":0.12*i+0.04/9*(i+1),"y":0.83}))
            else:
                self.add_widget(Label(
                    text=str(self.day_dates[i - 1].day) + '/' + str(self.day_dates[i - 1].month) + '\n    ' + weekday[
                        i - 1], font_size='20', size_hint=(0.12, 0.16), color=(0, 0, 0, 1),
                    pos_hint={"x": 0.12 * i + 0.04 / 9 * (i + 1), "y": 0.83}))

        for i in range(1, 8):
            event_in_same_day = 0
            for event in event_list:

                temp_month = event.date[-4:]
                temp_day = event.date[:-5]
                temp_month = temp_month.replace(' ','')
                if len(temp_day)>0:
                    if temp_day[0] == '0':
                        temp_day = temp_day[1]
                    temp_day = temp_day.replace(' ', '')

                if temp_day == str(self.day_dates[i-1].day) and temp_month == month_converter[str(self.day_dates[i-1].month)]:
                    event_in_same_day += 1

                    self.local_event_week_list.append(EventWeeklyLocalList(i,event_in_same_day, event.name, event.date, event.time, event.for_mat, event.course, event.location))

                    if len(event.name)>25:
                        temp_text = event.name[6:23] + '...'
                    else:
                        temp_text = event.name[6:]

                    if len(event.for_mat)>25:
                        temp_text = temp_text + '\n'+ event.for_mat[:23] + '...'
                    else:
                        temp_text = temp_text + '\n'+ event.for_mat
                    button_text = temp_text + '\n'+event.time
                    bgcolor = (0,0,0,1)#red(1,0,0,1)   (0.0235,0.5,0,1) green (0.196,0.6,1,1)blue  purple(0.6,0.196,1,1) pink (1,0.196,0.784,1) orange(1,0.549,0.196,1)
                    if event.course[8:16] == "MEDU2300":
                        bgcolor = (1,0,0,1)
                    if event.course[8:16] == "MEDU2400":
                        bgcolor = (0.0235,0.5,0,1)
                    if event.course[8:16] == "MEDU2600":
                        bgcolor = (1,0.196,0.784,1)
                    if event.course[8:16] == "MEDU2140":
                        bgcolor = (1,0.549,0.196,1)
                    if event.course[8:16] == "MEDU2500":
                        bgcolor = (0.196,0.6,1,1)
                    if event.course[8:16] == "":
                        bgcolor = (0.6,0.196,1,1)

                    btn = Button(text = button_text,font_size=7.2*Window.height/500 ,size_hint = (0.12,0.13), pos_hint = {"x":0.12*i+ 0.04 / 9 * (i + 1),"y":0.8-event_in_same_day*0.13}, background_color=bgcolor)
                    btn.background_normal = ''
                    self.add_widget(btn)




class EventViewBackground(FloatLayout):

    def __init__(self,**kwargs):
        super(EventViewBackground, self).__init__(**kwargs)
        self.draw()


    def on_touch_down(self, touch):
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0.78, 0,1)
            Rectangle(size=(Window.width, Window.height))
            Color(1,1,1,1)
            for i in range(1,8):
                Rectangle(size=(Window.width * 0.12, Window.height * 0.16),pos=(Window.width * 0.12 * i + Window.width * 0.04 / 9 * (i + 1), Window.height * 0.83))
                Rectangle(size=(Window.width*0.12,Window.height*0.8),pos=(Window.width*0.12*i + Window.width*0.04/9*(i+1), Window.height*0.02))
        btn = Button(text='MEDU2300 \n Human Structure I', background_color=(1, 0, 0, 1), size_hint=(0.12, 0.1),
                     pos_hint={"x": 0.04 / 9, "y": 0.6}, font_size=8)
        btn.background_normal = ''
        self.add_widget(btn)
        btn = Button(text='MEDU2400 \n Human Function I', background_color=(0.0235, 0.5, 0, 1), size_hint=(0.12, 0.1),
                     pos_hint={"x": 0.04 / 9, "y": 0.5}, font_size=8)
        btn.background_normal = ''
        self.add_widget(btn)
        btn = Button(text='MEDU2600 \n MMG', background_color=(1, 0.196, 0.784, 1),
                     size_hint=(0.12, 0.1),
                     pos_hint={"x": 0.04 / 9, "y": 0.4}, font_size=8)
        btn.background_normal = ''
        self.add_widget(btn)
        btn = Button(text='MEDU2140 \n Bioethics II', background_color=(1, 0.549, 0.196, 1), size_hint=(0.12, 0.1),
                     pos_hint={"x": 0.04 / 9, "y": 0.3}, font_size=8)
        btn.background_normal = ''
        self.add_widget(btn)
        btn = Button(text='MEDU2500 \n Doctor and Patient I', background_color=(0.196, 0.6, 1, 1),
                     size_hint=(0.12, 0.1),
                     pos_hint={"x": 0.04 / 9, "y": 0.2}, font_size=8)
        btn.background_normal = ''
        self.add_widget(btn)
        btn = Button(text=' \n N/A', background_color=(0.6, 0.196, 1, 1), size_hint=(0.12, 0.1),
                     pos_hint={"x": 0.04 / 9, "y": 0.1}, font_size=8)
        btn.background_normal = ''
        self.add_widget(btn)

class CalendarView(Screen):

    def add_event(self):
        self.add_widget(EventViewBackground())
        self.event_view_instance = EventView()
        self.add_widget(self.event_view_instance)


    def update_event(self):
        self.remove_widget(self.event_view_instance)
        self.event_view_instance = EventView()
        self.add_widget(self.event_view_instance)
        print(("hurray"))

    def __init__(self, **kwargs):
        super(CalendarView, self).__init__(**kwargs)
        self.add_event()

    def select_date(self):

        calendar_window = DateSelect(self)
        popup_window = Popup(title="Select Date", content=calendar_window, size_hint=(0.75,0.75))
        popup_window.open()



class MFPO(App):
    def build(self):

        return


if __name__ == "__main__":
    MFPO().run()
