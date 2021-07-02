"""
this module takes care of all the task that has to with delivering the lessons to the user
The format of the lesson should be as shown below when it is to be configured with a sound control object
[
	{
		"caption":"Name of file to speak the caption of the lesson to be delivered",
		"lesson":{
			"A key to be used in identifying the part on the map that was clicked":"Name of the file that contains the lesson to be delivered to the user based on the part of the map that was touched",
			"A key to be used in identifying the part on the map that was clicked":"Name of the file that contains the lesson to be delivered to the user based on the part of the map that was touched"
		}
	}
]

And below when it is to be configured with a Text to speech converter object

[
	{
		"caption":"Text to be spoken as the caption of the lesson",
		"lesson":{
			"A key to be used in identifying the part on the map that was clicked":"A text format of the lesson to be delivered (spoken) to the user based on the part of the map that was touched",
			"A key to be used in identifying the part on the map that was clicked":"A text format of the lesson to be delivered (spoken) to the user based on the part of the map that was touched"
		}
	}
]

"""

from speech_control import SoundControl as sc #importing the module that have been programmed to take care of sound
from text_converter import Converter as ct #importing the module that have been programmed to convert text to speech
import json


class Lesson(object):
	"""
	This class creates the instance for the quiz, a file is to be provided which has the record of all the audio files for each of the questions in the quiz
	and also the they correct option.
	"""
	def __init__(self, file):
		with open(file, 'r') as f:
			data = f.read()
		self.lessons = json.loads(data)
		
	def configure_with_sound_control(self):
		"""
		The method configures the lesson with a sound control object
		"""
		for le in self.lessons:
			le["caption"] = sc(le["caption"]) #reconfiguring the caption to a sound control object
			for key in le["lesson"].keys():
				le["lesson"][key] = sc(le["lesson"][key])#reconfiguring the lesson to a sound control object

		self.result_sayer = sc("audio_files/LESSON MODE.wav")# specifying the result sayer

	def configure_with_tts_converter(self):
		"""
		This method configures the lesson with a text to speech converter
		"""
		for le in self.lessons:
			le["caption"] = ct(le["caption"]) #reconfiguring the caption to a text to speech converter object
			for key in le["lesson"].keys():
				le["lesson"][key] = ct(le["lesson"][key])#reconfiguring the lesson to a text to speech converter object

		self.result_sayer = ct("LESSON MODE")# specifying the result sayer


	def get_lesson(self, id):
		"""
		This gets a particular lesson dict in the lessons and returns none if there is no lesson with the index of id
		"""
		if id < len(self.questions) and id >= 0:
			return self.questions[id]
		else:
			return None

	def next_lesson(self, id):
		"""
		This returns the next lesson dict in the lessons array
		"""
		if id < (len(self.lessons) - 1):
			return self.lessons[id+1]
		else:
			return None

	def previous_lesson(self, id):
		"""
		This returns the previous lesson and returns non if they is no previous lesson
		"""
		if id > 0:
			return self.lessons[id-1]
		else:
			return None
	def play_lesson(self, le):
		"""
		This plays the lesson

		Note: the quiz property of the object has to be set before this method is called else an error could be raised
		"""
		le["caption"].play(True) #playing the lesson
		choice = self.get_user_choice() #getting the user's choice
		while not (choice == "LESSON MODE" or choice == "QUIZ MODE"):#looping until the user wants to change the lesson or the mode
			"""
			This means that tapping the lesson button while the mode is already on lesson simply means the user wants to go to the next lesson
			"""
			if le["lesson"].get(choice): #checking if the user's choice of lesson is part of the lesson to be delivered
				le['lesson'][choice].play(True)#playing the lesson tied to that choice
			choice = self.get_user_choice() #getting the user's choice and also passing the mode so the hardware knows the current mode of operation
		next_lesson = self.next_lesson(self.lessons.index(le))
		if choice == "LESSON MODE":
			if next_lesson is not None:#checking if there is a next lesson
				return self.play_lesson(next_lesson)#playing the next lesson for the user
		else:
			return self.quiz.take_quiz()#taking quiz in a scenario where the user has selected quiz mode


	def get_user_choice(self):
		"""
		This method is meant to communicate to the hardware package and get the users response

		Note: the board has to be set before the method is called else it will raise an error
		"""
		result = self.board.get_touched()
		print(self.board.touched_pins)
		print(result)
		self.result_sayer.say(result)# saying the received result
		return result

	def take_lesson(self):
		"""
		This takes care of the lesson
		"""
		if len(self.lessons) > 0:#checking if there is a lesson at all to be played
			self.play_lesson(self.lessons[0])#playing the lesson
