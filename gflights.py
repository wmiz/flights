# Webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# Time
import time
import datetime

# Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Flight class
from flight import Flight

import sys, re, random

DEP_CITY = re.search(r"\w+", sys.argv[1]).group()
ARR_CITY = re.search(r"\w+", sys.argv[2]).group()
DEP_MONTH = re.search(r"--(\w+-\w+)", sys.argv[3]).group().split("-")
DEP_DATE = DEP_MONTH[2] + "-01-" + DEP_MONTH[3]
RETURN_DATE = "10-30-2020"
TICKET_TYPE = 1

# Email Credentials

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

def sleep(max_seconds):
	time.sleep(random.uniform(0, max_seconds))

def dep_city_chooser(dep_city):
	fly_from = browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[1]""")
	fly_from.click()
	fly_from = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input")
	fly_from.clear()
	sleep(1)
	fly_from.send_keys('  ' + dep_city)
	sleep(1)
	first_item = browser.find_element_by_xpath("""//*[@id='sbse0']/div[1]
		/div[1]/span[1]""")
	sleep(1)
	first_item.click()
	sleep(1)

def arrival_city_chooser(arrival_city):
	fly_to = browser.find_element_by_xpath("""//*[@id='flt-app']/div[2]
		/main[1]/div[4]/div/div[3]/div/div[2]/div[2]""")
	fly_to.click()
	fly_to = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input")
	fly_to.clear()
	sleep(1)
	fly_to.send_keys(' ' + arrival_city)
	sleep(1)
	first_item = browser.find_element_by_xpath("//*[@id='sbse0']/div[1]")
	sleep(1)
	first_item.click()
	sleep(1)

def dep_date_chooser(month, day, year):
	dep_date_button = browser.find_element_by_xpath("""//*[@id='flt-app']
		/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[4]/div[1]/div[2]""")
	dep_date_button.click()
	time.sleep(1)
	dep_date_button = browser.find_element_by_xpath("""//*[@id="flt-modaldialog"]
		/div/div[4]/div[2]/div[1]/date-input/input""")
	dep_date_button.send_keys(Keys.BACKSPACE)
	dep_date_button.send_keys(month + '/' + day + '/' + year)
	dep_date_button.send_keys(Keys.RETURN)
	time.sleep(4)
	price_els = browser.find_elements_by_css_selector(""".gws-travel-calendar__annotation""")
	price_els = [el for el in price_els if el.text != ""]
	sorted(price_els[:30], key=lowestPrice)[0].find_element_by_xpath("..").find_element_by_xpath("..").click()
	browser.find_element_by_xpath("""//*[@id="flt-modaldialog"]/div/div[5]/g-raised-button/div""").click()
	sleep(5)

def lowestPrice(price):
	if price.text == "":
		return 0
	else:
		return int(price.text[1:].replace(",", ""))


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
	sleep(10)
	print('Results ready!')


# Email functions
def connect_mail(username, password):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(username, password)

	return server

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
time.sleep(1)

# Set params for search
ticket_chooser(TICKET_TYPE)
dep_city_chooser(DEP_CITY)
arrival_city_chooser(ARR_CITY)
dep_date_params = DEP_DATE.split('-')
dep_date_chooser(dep_date_params[0], dep_date_params[1], dep_date_params[2])
if (TICKET_TYPE == 0):
	ret_date_params = RETURN_DATE.split('/')
	return_date_chooser(ret_date_params[0], ret_date_params[1], 
		ret_date_params[2])

# Create new flight object from seach
flight = Flight(DEP_CITY + " | " + ARR_CITY + " | " + DEP_DATE + " | " 
	+ RETURN_DATE)
flight.setDepCity(DEP_CITY)
flight.setArrCity(ARR_CITY)
time.sleep(1)

# Set flight object variables
# Departure time:
try:
	flight.setDep(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]
		/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]
		/div[1]/div/span[1]/span/span""").text)
except (NoSuchElementException, StaleElementReferenceException):
	time.sleep(1)
	browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]/div[7]
		/div[2]/div/div[2]/fill-button""").click()
	time.sleep(1)
	flight.setDep(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]
		/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]
		/div[1]/div/span[1]/span/span""").text)

try:
	flight.setArr(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]
	/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]
	/div[1]/div/span[2]/span/span[1]""").text)
except (NoSuchElementException, StaleElementReferenceException):
	time.sleep(1)
	browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]/div[7]
		/div[2]/div/div[2]/fill-button""").click()
	time.sleep(1)
	flight.setArr(browser.find_element_by_xpath("""//*//*[@id="flt-app"]/div[2]/main[4]
	/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]
	/div[1]/div/span[2]/span/span[1]""").text)

# Convert price then add to flight
price = (browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]
	/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[6]
	/div""").text)[1:]

c = CurrencyRates()

flight.setPrice("$" + price)

# Duration
flight.setDuration(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/
	main[4]/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]
	/div[3]/div[1]""").text)

# Stops
flight.setStops(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/main[4]
	/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[4]
	/div[1]/div/div[1]/span""").text.split()[0])

# Airline(s)
flight.setAirline(browser.find_element_by_xpath("""//*[@id="flt-app"]/div[2]/
	main[4]/div[7]/div[1]/div[13]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]
	/div[2]/div[2]/span[1]/span/span""").text)

# URL
flight.setURL(browser.current_url)

now = datetime.datetime.now()
current_date = (str(now.year) + '-' + str(now.month) + "-" + str(now.day))
current_time = (str(now.hour) + ':' + str(now.minute))
current_price = 'price' + '(' + current_date + '---' + current_time + ')'

msg = flight.create_msg()

f = open("saved/" + DEP_CITY + "_" + ARR_CITY + "_" + DEP_DATE + ".txt", "w")
f.write(msg)
f.close()

# Email

# server = connect_mail(USERNAME,PASSWORD)
# send_email(msg, server, flight)
# print('Email sent!')

# Delay

# time.sleep(3600)