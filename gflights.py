# Webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Time
import time
import datetime

# Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Flight class
from flight import Flight

DEP_CITY = "Pittsburgh"
ARR_CITY = "Rome"
DEP_DATE = "10/01/2019"
RETURN_DATE = "10/15/2019"
TICKET_TYPE = 1

# Email Credentials
USERNAME = 'wlmisback@gmail.com'
PASSWORD = 'Blu3Fi$h123'

#Currency Conversion
from forex_python.converter import CurrencyRates


#Scraper functions
def ticket_chooser(ticket):
	if ticket == 1:
		try:
			ticket_menu = browser.find_element_by_xpath("""//*[@id='flt-app']
				/div[2]/main[1]/div[4]/div/div[3]/div/div[1]/div[1]
				/dropdown-menu/div/div[1]/span[1]""")
			ticket_menu.click()
			time.sleep(1)
			ticket_type = browser.find_element_by_xpath("""//*[@id='flt-app']
				/div[2]/main[1]/div[4]/div/div[3]/div/div[1]/div[1]
				/dropdown-menu/div/div[2]/menu-item[2]/span""") 
			ticket_type.click()

		except Exception as e:
			print("Error finding flight type element")
			pass
	else:
		pass

def dep_city_chooser(dep_city):
	fly_from = browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
		/main[1]/div[4]/div/div[3]/div/div[2]/div[1]""")
	fly_from.click()
	fly_from = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input")
	fly_from.clear()
	time.sleep(1.5)
	fly_from.send_keys('  ' + dep_city)
	time.sleep(1.5)
	first_item = browser.find_element_by_xpath("""//*[@id='sbse0']/div[1]
		/div[1]/span[1]""")
	time.sleep(1.5)
	first_item.click()
	time.sleep(1)

def arrival_city_chooser(arrival_city):
	fly_to = browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
		/main[1]/div[4]/div/div[3]/div/div[2]/div[2]""")
	fly_to.click()
	fly_to = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input")
	fly_to.clear()
	time.sleep(1.5)
	fly_to.send_keys(' ' + arrival_city)
	time.sleep(1.5)
	first_item = browser.find_element_by_xpath("//*[@id='sbse0']/div[1]")
	time.sleep(1.5)
	first_item.click()
	time.sleep(1)

def dep_date_chooser(month, day, year):
	dep_date_button = browser.find_element_by_xpath("""//*[@id='flt-app']
		/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[4]/div[1]/div[2]""")
	dep_date_button.click()
	time.sleep(1)
	dep_date_button = browser.find_element_by_xpath("""//*
		[@id='flt-modaldialog']/div/div[4]/div[2]/div[1]/date-input/input""")
	dep_date_button.send_keys(Keys.BACKSPACE)
	dep_date_button.send_keys(month + '/' + day + '/' + year)

def return_date_chooser(month, day, year):
	return_date_button = browser.find_element_by_xpath("""//*
		[@id='flt-modaldialog']/div/div[4]/div[2]/div[3]/date-input/input""")
	
	for i in range(11):
		return_date_button.send_keys(Keys.BACKSPACE)
	return_date_button.send_keys(month + '/' + day + '/' + year)
	return_date_button.send_keys(Keys.ESCAPE)

def search():
	search = browser.find_element_by_xpath("""//*[@id='flt-modaldialog']/div
		/div[5]/g-raised-button""")
	search.click()
	time.sleep(10)
	print('Results ready!')


# Email functions
def connect_mail(username, password):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(username, password)

	return server

# Create message template for email
def create_msg(flight):
	msg = """Departure time: {}\nArrival time: {}\nAirline: {}
	\nFlight duration: {}\nNo. of stops: {}\n
	Price: {}\n""".format(flight.getDep(),
		   flight.getArr(),
		   flight.getAirline(),
		   flight.getDuration(),
		   flight.getStops(),
		   flight.getPrice())
	return msg

def send_email(msg, server, flight):
	message = MIMEMultipart()
	message['Subject'] = flight.getName()
	message['From'] = 'wlmisback@gmail.com'
	message['To'] = 'wlmisback@gmail.com'
	message.attach(MIMEText(msg, 'plain'))

	server.sendmail('wlmisback@gmail.com', 'wlmisback@gmail.com', 
		message.as_string())



#Create webdriver
browser = webdriver.Chrome(executable_path='chromedriver')

#Set up search
#Delete webdriver cookies
browser.delete_all_cookies()
link = 'https://www.google.com/flights?hl=en'
browser.get(link)
time.sleep(5)

# Set params for search
ticket_chooser(TICKET_TYPE)
dep_city_chooser(DEP_CITY)
arrival_city_chooser(ARR_CITY)
dep_date_params = DEP_DATE.split('/')
dep_date_chooser(dep_date_params[0], dep_date_params[1], dep_date_params[2])
if (TICKET_TYPE == 0):
	ret_date_params = RETURN_DATE.split('/')
	return_date_chooser(ret_date_params[0], ret_date_params[1], 
		ret_date_params[2])

# Do Search
search()

# Create new flight object from seach
flight = Flight(DEP_CITY + " | " + ARR_CITY + " | " + DEP_DATE + " | " 
	+ RETURN_DATE)
flight.setDepCity(DEP_CITY)
flight.setArrCity(ARR_CITY)

# Set flight object variables
# Departure time
flight.setDep(browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]/main[4]
	/div[7]/div[1]/div[5]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]
	/div[1]/div/span[1]/span/span""").text)

# Arrival time
flight.setArr(browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
	/main[4]/div[7]/div[1]/div[5]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]
	/div[1]/div[2]/div[1]/div/span[2]/span/span[1]""").text)

# Convert price then add to flight
EUR_price = (browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
	/main[4]/div[7]/div[1]/div[5]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]
	/div[1]/div[5]/div""").text)[1:]

c = CurrencyRates()
USD_price = str(round(c.convert('EUR', 'USD', int(EUR_price)), 2))

flight.setPrice("$" + USD_price)

# Duration
flight.setDuration(browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
	/main[4]/div[7]/div[1]/div[5]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]
	/div[1]/div[3]/div[1]""").text)

# Stops
flight.setStops(browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
	/main[4]/div[7]/div[1]/div[5]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]
	/div[1]/div[4]/div[1]/div/div/span""").text)

# Airline(s)
flight.setAirline(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]
	/main[4]/div[7]/div[1]/div[5]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]
	/div[1]/div[2]/div[2]/span[2]/span/span/span/span/span""").text)

now = datetime.datetime.now()
current_date = (str(now.year) + '-' + str(now.month) + "-" + str(now.day))
current_time = (str(now.hour) + ':' + str(now.minute))
current_price = 'price' + '(' + current_date + '---' + current_time + ')'

msg = create_msg(flight)
server = connect_mail(USERNAME,PASSWORD)
send_email(msg, server, flight)
print('Email sent!')

# time.sleep(3600)