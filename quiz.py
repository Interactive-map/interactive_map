"""
this module takes care of all the task that has to do with taking the quiz
The format of the question should be as shown below when it is to be configured with a sound control object
[
	{
		"question":"filename of question", 
		"correct":"A key to be used in retrieving the correct answer from the sensor package",
		"on_wrong":"filename of audio to play if the user gets the question wrongly", 
		"return_on_wrong":"integer specifying question to return to if user chooses wrong option to question",
		"on_correct":"filename of audio to play if the user gets the question correctly right",
		"return_on_correct":"integer of quesiton to return to if the user chooses the correct option"
	},
]

And below when it is to be configured with a Text to speech converter object

[
	{
		"question":"The question in text format", 
		"correct":"A key to be used in retrieving the correct answer from the sensor package",
		"on_wrong":"Text to be spoken to the user if the user gets the question wrongly", 
		"return_on_wrong":"integer specifying question to return to if user chooses wrong option to question",
		"on_correct":"Text to be spoken to the user if the user gets the question correctly",
		"return_on_correct":"integer of quesiton to return to if the user chooses the correct option"
	},
]

"""
from speech_control import SoundControl as sc #importing the module that have been programmed to take care of sound
from text_converter import Converter as ct #importing the module that have been programmed to convert text to speech
import json


speech = ct("Touch the states and receive a reply from us")

class Quiz(object):
	"""
	This class creates the instance for the quiz, a file is to be provided which has the record of all the audio files for each of the questions in the quiz
	and also the they correct option.
	"""
	def __init__(self, file):
		with open(file, 'r') as f:
			data = f.read()
		self.questions = json.loads(data)
		
	def configure_with_sound_control(self):
		"""
		The method configures the quiz with a sound control object
		"""
		for q in self.questions:
			q["question"] = sc(q["question"]) #reconfiguring the question to a sound control object
			if not q.get("on_wrong") == None: #making sure that the on_wrong option is not set to None befor setting it be a sound control object
				q["on_wrong"] = sc(q["on_wrong"])
			if not q.get("on_correct") == None: #making sure that the on_correct option is not set to None befor setting it to be a sound control object
				q["on_correct"] = sc(q["on_correct"])

	def configure_with_tts_converter(self):
		"""
		This method configures the quiz with a text to speech converter
		"""
		for q in self.questions:
			q["question"] = ct(q["question"]) #reconfiguring the question to a text to speech converter object
			if not q.get("on_wrong") == None: #making sure that the on_wrong option is not set to None befor setting it be a text to speech converter object object
				q["on_wrong"] = ct(q["on_wrong"])
			if not q.get("on_correct") == None: #making sure that the on_correct option is not set to None befor setting it to be a text to speech converter object
				q["on_correct"] = ct(q["on_correct"])

	def get_question(self, id):
		"""
		This gets a particular question in the quiz and returns none if there is no question with that id
		"""
		if id < len(self.questions) and id >= 0:
			return self.questions[id]
		else:
			return None

	def next_question(self, id):
		"""
		This returns the next question in the quiz
		"""
		if id < (len(self.questions) - 1):
			return self.questions[id+1]
		else:
			return None

	def previous_question(self, id):
		"""
		This returns the previous question and returns non if they is no previous question
		"""
		if id > 0:
			return self.questions[id-1]
		else:
			return None
	def play_question(self, q):
		"""
		This plays the question
		Note: the lesson property of the object has to be set before calling this method else this method could raise an error
		"""
		q["question"].play(True) #playing the question
		choice = self.get_user_choice() #getting the user's choice
		next_question = self.next_question(self.questions.index(q))
		if choice == "LESSON MODE":
			self.lesson.take_lesson()
		elif choice == "QUIZ MODE":
			if next_question is not None:
				return self.play_question(next_question)
		elif choice == q["correct"]: #checking if choice is correct
			if q.get('on_correct') is not None:
				q['on_correct'].play(True)
			if q.get('return_on_correct') is not None:
				return self.play_question(q['return_on_correct'])
		elif q.get('return_on_wrong') is not None: #in case choice is not correct
			if q.get('on_wrong') is not None:
				q['on_wrong'].play(True)
			if q.get('return_on_wrong') is not None:
				return self.play_question(q['return_on_wrong'])
		elif q.get('on_wrong') is not None:
			q['on_wrong'].play(True)
		
		if next_question is not None:
			return self.play_question(next_question)

	def get_user_choice(self):
		"""
		This method is meant to communicate to the hardware package and get the users response
		Note the board property has to be set before this method is called, else the method will raise an error
		"""
		result = self.board.get_touched()
		print(self.board.touched_pins)
		print(result)
		speech.say(result)
		return result

	def take_quiz(self):
		"""
		This takes care of the quiz
		"""
		if len(self.questions) > 0: #checking to make sure that the quiz is not empty
			self.play_question(self.questions[0])


