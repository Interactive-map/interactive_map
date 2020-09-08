import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mpr121.MPR121(i2c)

class Sensor:
	"""
	This class handles the sensor implementations
	"""
	def __init__(self, touch_data):
		"""
		Initializes the board and other parameters.
		the touch_data parameter to be provided should be in the below format
		states = {
			"Abuja":{1, 2},#set for pin combination for this state
			"Ebonyi":{3,4,6}
		}
		"""
		self.touch_data = touch_data #this is the data stating the touch combinations
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.mpr = adafruit_mpr121.MPR121(i2c)

	def get_touched_pins(self):
		"""
		this method returns the touched pins at the instance it is called
		"""
		touched = set()#creating a set to hold the touched pins
		for i in range(12):#looping through the available pins in the MPR121 sensor
			if self.mpr[i].value:#checking if pin is active, i.e if pin is touched
				touched.add(i)#adding the pin to the set of touched pins 
		return touched

	def get_keyword_from_pins(self, pins):
		"""
		This method returns the state keyword in the touch_data that has the pin combination provided by the pins parameter
		It returns None if no state with such pin combination is found.
		"""
		for key in self.touch_data.keys:#looping through the states in the touch_data which are keys in the touch_data dictionary
			if pins = self.touch_data[key]:
				return key
		return None

	def is_active(self, keyword):
		"""
		This method returns the touch state of a given keyword in the touch_data using the keyword parameter as the key for the 
		keyword to get it's touch state. 
		The method returns false if not touched and true if touched
		"""
		if self.get_keyword_from_pins(self.get_touched_pins()) == key:#checking if keyword represented by touched pins = keyword being checked
			return True
		else:
			return False