class Flight:
	# Holds flight data
	def __init__(self, name):
		self.name = name

	#Setter methods
	def setDep(dep_time):
		self.dep_time = dep_time
	def setArr(arr_time):
		self.arr_time = arr_time
	def setAirline(airline):
		self.airline = airline
	def setPrice(price):
		self.price = price
	def setDuration(duration):
		self.duration = duration
	def setStops(stops):
		self.stops = stops
	def setLayovers(layovers):
		self.layovers = layovers

	#Getter methods
	def getDep():
		return self.dep_time
	def setArr():
		return self.arr_time
	def getAirline():
		return self.airline
	def getPrice():
		return self.price
	def getDuration():
		return self.duration
	def getStops():
		return self.stops
	def getLayovers():
		return self.layovers


