# This module will drive the gflights.py module. It will take a number of current
# locations and desired destinations and desired months of travel. From this information
# it will build a spreadsheet of the cheapest available flights
import sys, re

# First parse arguments

if len(sys.argv) == 1:
	print("""Improper number of arguments! 
		Command should look like 'python3 gflightsdriver.py --curr city1 city2 
		etc... --dest region1 region2 etc... --date 01/2021 02/2021 etc...""")
	quit()

del sys.argv[0]
ops = " ".join(sys.argv)
ops = re.findall(r"--([\w\s/]+)", ops)
ops = [op.strip() for op in ops]							# Trim whitespace

setup = {}

for op in ops:
	op = op.split(" ")
	setup[op[0]] = op[1:]

print(setup)

