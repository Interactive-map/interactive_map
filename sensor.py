import time
import serial

class Sensor:
	"""
	This class handles the sensor implementations
	"""
	RESET_PIN = '8'
	LESSON_MODE_PINS = {'9'}#the pins that when touched together, it means the user wants to select lesson mode
	QUIZ_MODE_PINS = {'10'}#the pins that when touched together, it means the user wants to select quiz mode
	CURRENT_MODE = "LESSON MODE"#setting that the default mode is lesson mode
	def __init__(self, touch_data, com_port, baud_rate=9600, timeout=0.1):
		"""
		Initializes the board and other parameters.
		the touch_data parameter to be provided should be in the below format
		states = {
			"Abuja":{1, 2},#set for pin combination for this state
			"Ebonyi":{3,4,6}
		}
		"""
		self.touch_data = touch_data #this is the data stating the touch combinations
		self.board = serial.Serial(com_port, baud_rate, timeout=timeout)#getting the serial port the arduino is communicating from
		self.looping = False #this variable states if the event loop is on or not
		self.touched_pins = set() #this is to hold the set of pins that have been touched

	def get_touched_pins(self):
		"""
		this method returns the touched pins at the instance it is called
		"""
		return set(self.board.readline()[:-2].decode().split(' ')[1:])
	def update_status(self):
		"""
		This method updates the status of the touched pin
		"""
		self.touched_pins.clear()#reseting the touched pins
		array_of_pins = self.board.readline()[:-2].decode().split(' ')#retrieving the pins and there touch status
		for pin in array_of_pins:#looping through the array of pins in order to update the touched_pins
			if "Touched" in pin:#checking if this is a pin that was just touched
				pin_num = pin.split("-")[1]#retrieving the pin number
				self.touched_pins.add(pin_num)#adding the pin number to the set of touched pins
			elif "Released" in pin:#checking if the pin was released instead of touched
				pin_num = pin.split("-")[1]#retrieving the pin number
				if pin_num in self.touched_pins:#checking if the pin number already exist in the set of touched pins before attempting to remove it
					self.touched_pins.remove(pin_num)#removing the pin number from the set of touched pins
	def analyze(self):
		"""
		This method analyze the touched_pins to know what part of the map that was touched
		"""
		key = None
		if self.RESET_PIN in self.touched_pins:#checking if the pin for reseting was touched
			self.confirm()#asking the user to confirm the attempt to reset the map
			self.update_status()#updating the status of the touched_pins first
		elif self.LESSON_MODE_PINS == self.touched_pins:#checking if the pins touched are those of the lesson mode
			key = "LESSON MODE"#setting that the key is LESSON_MODE
			self.update_status()#updating the status of the touched_pins first
		elif self.QUIZ_MODE_PINS == self.touched_pins:#checking if the pins touched are those of the quiz mode
			key = "QUIZ MODE"#setting that the key is QUIZ_MODE
			self.update_status()#updating the status of the touched_pins first
		else:
			key = self.get_keyword_from_pins()
		return key
	def get_touched(self):
		"""
		This method gets the touched parts in the map
		"""
		state = None#holds the state that was touched
		while state is None:#looping until a touched state is found
			state = self.analyze()#reseting the state to be the output of the analysis on the touched pins
		else:
			return state# returning the state if a touched stat is found
	def confirm(self):
		"""
		This method asks the user to confirm an attempt to perform a given operation
		"""
		return None
	def get_keyword_from_pins(self, pins=False):
		"""
		This method returns the state keyword in the touch_data that has the pin combination provided by the pins parameter
		It returns None if no state with such pin combination is found.
		"""
		if not pins:
			self.update_status()#updating the status of the touched_pins first
			pins = self.touched_pins#setting the pins to be the touched pins if there is no pins provided
		for key in self.touch_data.keys():#looping through the states in the touch_data which are keys in the touch_data dictionary
			if pins == self.touch_data[key]:
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
	def start_loop(self):
		"""
		this method starts the loop for listening and writing to the arduino microcontroller communication
		"""
		self.looping = True #setting the looping varialbe to true so that it can be used as a control for the looping
		#while self.looping:

