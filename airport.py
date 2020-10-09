class Airport:
	# Holds flight data
	def __init__(self, code):
		self.code = code

	def setCode(self, code):
		self.code = code

	def setName(self, name):
		self.name = name

	def setCountry(self, country):
		self.country = country

	def setCity(self, city):
		self.city = city


	def getCode(self):
		return self.code

	def getName(self):
		return self.name

	def getCountry(self):
		return self.country

	def getCity(self):
		return self.city

	def isMatch(self, string):
		return self.code.lower() == string.lower() or self.name.lower() == string.lower() or self.country.lower() == string.lower() or self.city.lower() == string.lower()