from selenium import webdriver
from bs4 import BeautifulSoup
import csv

def update_calendar(starting_Date, ending_Date):
    #open chrome and login to mfpo
    s_date = starting_Date
    e_date = ending_Date
    print(s_date)
    print(e_date)

    driver = webdriver.Chrome()
    driver.get("https://intranet.mfpo.cuhk.edu.hk/med/timetable/index.aspx")
    pwd = driver.find_element_by_name("Password")
    usr = driver.find_element_by_name("UserName")
    pwd.send_keys("vlbs@123")
    usr.send_keys('1155143214@link.cuhk.edu.hk')
    driver.find_element_by_id("submitButton").click()

    #temp

    #change date to appropriate day
    driver.get("https://intranet.mfpo.cuhk.edu.hk/med/Timetable/StudentDailyEventViewer.aspx")
    currentDate = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtDate").get_attribute("value")

    for letter in currentDate:
        currentDate = currentDate.replace("-", '')
    if currentDate[0] == '0':
        currentDate = currentDate[1:]

     #//////////////////////////////////////////////////////////////////////////////////////////


    def check_calendar_year(required_date):
        if int(currentDate[-4:]) < int(required_date[-4:]):
            return 3
        elif int(currentDate[-4:]) > int(required_date[-4:]):
            return 1
        else:
            return 2


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


    def change_date(required_dates):
        required_date = required_dates
        if currentDate == required_date:
            return
        driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtDate").click()
        driver.find_element_by_xpath("//th[@class='datepicker-switch']").click()
        if check_calendar_year(required_date) != 2:
            press_count = abs(int(required_date[-4:]) - int(currentDate[-4:]))
            for i in range(0, press_count):
                if check_calendar_year(required_date) == 3:
                    driver.find_element_by_xpath("//div[@class='datepicker-months']/table/thead/tr/th[@class='next']").click()
                if check_calendar_year(required_date) == 1:
                    driver.find_element_by_xpath("//div[@class='datepicker-months']/table/thead/tr/th[@class='prev']").click()

        month_button_list = driver.find_elements_by_xpath("//span[@class='month']")
        tempx = driver.find_element_by_xpath("//span[@class='month active']")
        if tempx!= None:
            month_button_list.append(tempx)
        for button in month_button_list:
            if button.text == required_date[-7:-4]:
                button.click()
                break
        day_button_list = driver.find_elements_by_xpath("//td[@class='day']")
        if currentDate[-7:-4] == required_date[-7:-4]:

            temp = driver.find_element_by_xpath("//td[@class='active day']")
            if temp != None:
                day_button_list.append(temp)
        for buttonX in day_button_list:
            if buttonX.text == required_date[:-7]:
                buttonX.click()
                break


    def start_scrape(starting_date, ending_date):
        #start scraping
        writer = csv.writer(database, lineterminator='\n')
        writer.writerow((['Name', 'Date', 'Time', 'Format', 'Location', 'Course']))
        change_date(starting_date)
        currentDate = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtDate").get_attribute("value")
        for letter in currentDate:
            currentDate = currentDate.replace("-", '')
        if currentDate[0] == '0':
            currentDate = currentDate[1:]


        record = open("UpdateRecord.txt", "w")
        record.write("From " + currentDate + " to ")
        while currentDate != ending_date:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            #scraping course info
            currentDate = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtDate").get_attribute("value")
            for letter in currentDate:
                currentDate = currentDate.replace("-", '')
            if currentDate[0] == '0':
                currentDate = currentDate[1:]

            event_count = len(soup.find_all('i', class_='fa fa-clock-o'))
            for i in range(0, event_count):
                info_d_t = soup.find_all('i', class_="fa fa-clock-o")[i].find_next_sibling("h4")
                info = soup.find_all('i', class_='fa fa-clock-o')[i].find_next_siblings("p")
                if(len(info)>0):

                    course = info[0].text
                if(len(info)>1):
                    for_mat = info[1].text
                if (len(info) > 2):
                    name = info[2].text
                if (len(info) > 3):
                    location = info[3].text
                else:
                    course = ''
                    for_mat = ''
                    name = ''
                    location = ''
                if(info_d_t!=None):
                    date = info_d_t.text[:-11]
                    time = info_d_t.text[-11:]
                else:
                    date = ''
                    time = ''
                writer.writerow([name, date, time, for_mat, location, course])
            driver.find_element_by_xpath("//input[@class='btn btn-info']").click()

        record.write(ending_date)
        record.close()
     #//////////////////////////////////////////////////////////////////////////////////////////



    database = open("Database.csv", "w")
    start_scrape(s_date, e_date)

    database.close()

    driver.close()


