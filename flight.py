class Flight:
	# Holds flight data
	def __init__(self, name):
		self.name = name

	#Setter methods
	def setDepCity(self, dep_city):
		self.dep_city = dep_city
	def setArrCity(self, arr_city):
		self.arr_city = arr_city
	def setDep(self, dep_time):
		self.dep_time = dep_time
	def setArr(self, arr_time):
		self.arr_time = arr_time
	def setAirline(self, airline):
		self.airline = airline
	def setPrice(self, price):
		self.price = price
	def setDuration(self, duration):
		self.duration = duration
	def setStops(self, stops):
		self.stops = stops

	#Getter methods
	def getName(self):
		return self.name
	def getDep(self):
		return self.dep_time
	def getArr(self):
		return self.arr_time
	def getAirline(self):
		return self.airline
	def getPrice(self):
		return self.price
	def getDuration(self):
		return self.duration
	def getStops(self):
		return self.stops


