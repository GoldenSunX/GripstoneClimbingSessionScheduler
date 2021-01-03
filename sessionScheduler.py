"""Step by  step instructions for booking a session at https://gripstonecs.com/covid/ => https://app.rockgympro.com/b/widget/?a=offering&offering_guid=5f3a5588c2ea45ba94db31df7f282894&widget_guid=4ce4ab68c8d748058a6f0784c771a661&random=5feb70f0193b9&iframeid=rgpiframe5feb6ff338c88&mode=e
    0. Create participantInfo map (from ParticipantInfo.txt) and ask user for required variables
    1. Navigate to the app.rockgympro.com address from above
    ***
    2. Change the participants dropdown (id='pcount-pid-1-1136') to the desired number of participants 
    3. Select the desired date from the calendar component
    4. Identify the Select button associated with the desired time 
    5. For each <div class="booking-details-participant-info-block"> select the desired participant button (participants-btn btn) from the map in order then click the continue button (class="btn navforward")
    6. For each <input type="checkbox" data-required-checkbox="1"> change value to true then click complete booking button (id="confirm_booking_button")
    *  Bonus: schedule script execution for specefic date and time (1 week before desired 2 hour session)
"""

import selenium.webdriver
import time as tim
from datetime import datetime, date, time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Class Definitions

class Birthdate:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year
        
class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last
        
class Participant:
    def __init__(self, id, name, birthdate):
        self.id = id
        self.name: Name = name
        self.birthdate: Birthdate = birthdate
        
    def stateYourself(self):
        print("\nID: " + str(self.id) +
              "\nName: " + str(self.name.last) + ", " + str(self.name.first) +
              "\nBirthdate: " + str(self.birthdate.month) + " " + str(self.birthdate.day) + " " + str(self.birthdate.year))
        
# Creating the Dictionary of Participants from local file

participantDictionary = {}
participantInfo = open("ParticipantInfo.txt", "r")
for participant in participantInfo:
    pArray = participant.replace("\n", "").split(",")
    pID = int(pArray[0])
    pName = Name(pArray[1], pArray[2])
    pBirthdate = Birthdate(pArray[4], int(pArray[3]), int(pArray[5]))
    pParticipant = Participant(pID, pName, pBirthdate)
    participantDictionary[pID] = pParticipant
participantInfo.close()
# print(participantDictionary.get(1).stateYourself())

# Ask User for required variables
'''Variables the script requires:
    * Who is climbing (entered by ID)
    * Calendar date of session
    * Time of session
'''
# whoIsClimbing = input("Enter who is climbing by ID;\nBrandon:    0\nSam:        1\nAndrew:     2\nAlex:       3\nMike:       4\nAlyvia:     5\nBlank for default session.\n")
whoIsClimbing = ''
climbingGroup = []
if whoIsClimbing == '': # should consider bad input at some point
    climbingGroup = [1, 2, 3, 4]
else:
    for id in whoIsClimbing:
        climbingGroup.append(int(id))
        
# whatDateIsClimbing = input("Enter the date of the session (11/20): ")
whatDateIsClimbing = '01/07'
climbDate = date(date.today().year, int(whatDateIsClimbing[:2]), int(whatDateIsClimbing[-2:]))
dayOfWeek = climbDate.weekday()
sessionInfo = ''
if dayOfWeek == 1 | dayOfWeek == 3:
    sessionInfo = open('TuesdayAndThursdaySessions.txt', 'r')
elif dayOfWeek >= 5:
    sessionInfo = open('WeekendSessions.txt', 'r')
else:
    sessionInfo = open('WeekdaySessionTimes.txt', 'r')
sessionInfo.close()

# whatTimeIsClimbing = input("Enter the start time of the session (i.e. 6pm OR 8am)\n" + sessionInfo.read() + "\n")
whatTimeIsClimbing = '2pm'
whatTimeIsClimbingCAP = whatTimeIsClimbing.capitalize()
# print(int(whatTimeIsClimbing[:-2]) == 12)
# print(whatTimeIsClimbing[-2] == 'a')
climbTime = ''
if (whatTimeIsClimbing[-2] == 'a') | (int(whatTimeIsClimbing[:-2]) == 12): # does not consider all possible time entries and input is not filtered also doesn't consider the valid time options
    climbTime = time(int(whatTimeIsClimbing[:-2]))
else:
    climbTime = time(int(whatTimeIsClimbing[:-2])+12)
combinedClimbTime = datetime.combine(climbDate, climbTime)

# print(datetime.strftime(climbDate, '%B'))

# TODO: create a variable that can hold the morning or afternoon status as well as the hour, 24 hour time? probably not since you would convert it then convert it back

# Accessing the webpage 
from selenium.webdriver import Chrome 
with Chrome() as driver:
    driver.get('https://app.rockgympro.com/b/widget/?a=offering&offering_guid=66ab43ac5a344fe096dad3730fb9e538&widget_guid=4ce4ab68c8d748058a6f0784c771a661&random=5fef70e626bc4&iframeid=rgpiframe5fef6fb657581&mode=e')
    htmlPage = driver.find_element_by_tag_name('html')
    htmlPage.send_keys(Keys.END)
    # htmlPage.send_keys(Keys.chord(Keys.CONTROL, Keys.SUBTRACT))
    # htmlPage.send_keys(Keys.END)
    
    # tim.sleep(10)
    
    selectElement = driver.find_element_by_id('pcount-pid-1-1136')
    participantSelect = Select(selectElement)
    participantSelect.select_by_value(str(len(climbingGroup)))
    currentMonthElement = driver.find_element_by_class_name('ui-datepicker-month')
    if currentMonthElement.text != datetime.strftime(climbDate, '%B'):
        nextMonthElement = driver.find_element_by_class_name('ui-datepicker-next')
        nextMonthElement.click()
    availableDayElements = driver.find_elements_by_class_name('datepicker-available-day')
    for day in availableDayElements:
        # print('Element text')
        # print(day.text)
        # print('Formatted date to string removing the leading 0')
        # print(str(datetime.strftime(climbDate, '%d')).lstrip('0'))
        if day.text == str(datetime.strftime(climbDate, '%d')).lstrip('0'):
            # print('day is available')
            day.click()
            break
        # else:
        #     print('day is unavailable')
    
    
    # sessionTableElement = driver.find_element_by_class_name('offering-page-select-events-table')
    # print(sessionTableElement.text)
    
    
    # Logging in Attempt
    # aTagButtons = driver.find_elements_by_tag_name('a')
    # for button in aTagButtons:
    #     if button.text == 'Log In or Create Profile':
    #         button.click()    
    # # driver.find_element_by_id('rgp00-close-button').click()
    # emailInput = driver.find_element_by_name('email')
    # pInput = driver.find_element_by_id('inputPassword')
    # emailInput.send_keys('yingerCS42@gmail.com')
    # pInput.send_keys('Io9Um1KxEpJm')
    # aTagButtons = driver.find_elements_by_tag_name('a')
    # for button in aTagButtons:
    #     if button.text == 'Log In                ':
    #         button.click()
    
    # Find Availabel sessions
    # scheduleTableDiv = driver.find_element_by_id('containing-div-for-event-table')
    # tableRows = scheduleTableDiv.find_elements_by_tag_name('tr')
    # for row in tableRows:
    #     tableColumns = row.find_elements_by_tag_name('td')
    #     for column in tableColumns:
    #         print(column.text)
    driver.execute_script("document.body.style.zoom='50%'")
    tim.sleep(30)
    sessionElements = driver.find_element_by_id("offering-page-schedule-list-time-column")
    # print(sessionElements[0].text.split(',')[2])
    for session in sessionElements:
        sessionRow = session.text.split(',')[2].split(' ')[1] + session.text.split(',')[2].split(' ')[2].lower()
        if sessionRow == whatTimeIsClimbingCAP:
            sessionRow = sessionElements.index(session)
            bookNowButtons = driver.find_elements_by_class_name('book-now-button')
            bookNowButtons[sessionRow].click()
            break
    
    
    
    # html = driver.find_element_by_tag_name('html')
    # html.send_keys(Keys.END)
    # driver.execute_script("window.scrollTo(0, 4000)")
    driver.save_screenshot('screenshot.png')
    
    # driver.find_element()
#cheese = driver.find_element(By.ID, 'pcount-pid-1-1136')