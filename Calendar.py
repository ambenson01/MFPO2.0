import csv
from calendar import  Calendar
from datetime import date


class Event:
    def __init__(self, name, date, time, for_mat, location, course):
        self.name = name
        self.date = date
        self.time = time
        self.for_mat = for_mat
        self.location = location
        self.course = course


def initialize():

    database = open("Database.csv", "r")
    csv_reader = csv.reader(database, delimiter=',')
    line_count = -1  #also equal to number of events
    event_list = []
    for row in csv_reader:
        if line_count == -1:
            line_count =+ 1
        else:
            new_event = Event(row[0], row[1], row[2], row[3], row[4], row[5])
            event_list.append(new_event)
            line_count =+ 1
    database.close()
    return event_list

def find_today_date():
    today = date.today().strftime("%b-%d-%Y")
    today = today.replace('-', '')
    today_month = today[:3]
    today_year = today[-4:]
    today_day = today[3:-4]
    if today_day[0] == '0':
        today_day = today_day[1]
    return [today_day, today_month, today_year]

monthConverter ={
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        "Jun": 6,
        "Jul": 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }


def build_calendar(year, month):
    month_to_number = monthConverter[month]
    app_calendar = Calendar(6)
    day_list=[]
    for day in app_calendar.itermonthdays(year, month_to_number):
        day_list.append(day)
    return day_list


def find_current_week_dates(year, month, day):
    month_to_number = monthConverter[month]
    app_calendar = Calendar(6)
    day_list =[]
    week_no=0
    for dayx in app_calendar.itermonthdates(year, month_to_number):
        day_list.append(dayx)
    print(day_list)
    i=0
    for day2 in day_list:
        print(day2.day)
        if day2.day == day:
            week_no = i//7 +1
            break
        i+=1

    print(week_no)
    j=0
    wk=1
    retrn_list =[]
    for day3 in day_list:
        j+=1
        if wk == week_no:
            retrn_list.append(day3)
        if j == 7:
            j = 0
            wk+=1
        if wk>week_no:
            break

    return retrn_list


print(initialize()[0].date)










