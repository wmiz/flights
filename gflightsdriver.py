# This module drives the gflights.py module. It takes a number of current
# locations and desired destinations and desired months of travel. From this information
# it builds a spreadsheet of the cheapest available flights

import sys, re
import os
from airport import Airport


def checkExists(place, airports):
	for airport in airports:
		if airport.isMatch(place):
			return True

# First parse arguments

if len(sys.argv) == 1:
	print("""Improper number of arguments! 
		Command should look like 'python3 gflightsdriver.py --curr city1 city2 
		etc... --dest region1 country1 city1 etc... --date 01/2021 02/2021 etc...""")
	quit()

del sys.argv[0]
ops = " ".join(sys.argv)
ops = re.findall(r"--([\w\s/]+)", ops)
ops = [op.strip() for op in ops]							# Trim whitespace

setup = {}

for op in ops:
	op = op.split(" ")
	setup[op[0]] = op[1:]

#print(setup)

# Load all airports
print("Loading airports...")
regions = os.listdir("airport_codes")

airports = []

for region in regions:
	f = open("airport_codes/" + region, "rU")
	text = f.read()

	# Separate out relevant data
	airport_data = re.findall(r"\w+\s+(\w+)\s([\w ]+)\s+([\w ]+)\s+([\w ]+)\n", text)

	# Add each to airport list
	for airport_datum in airport_data:
		airport = Airport(airport_datum[0])
		airport.setName(airport_datum[1])
		airport.setCity(airport_datum[2])
		airport.setCountry(airport_datum[3])

		airports.append(airport)

# Check if arguments are valid

print("Checking validity of arguments...")
places = setup["curr"] + setup["dest"]
valid = True

for place in places:

	if not checkExists(place, airports):
		print ("Error: " + place + " is not valid.")
		valid = False
	else:
		print("Found " + place + " successfully!")

if not valid:
	print("Quitting...")
	quit()

# Run gflights.py with provided arguments
