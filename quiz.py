"""
this module takes care of all the task that has to do with taking the quiz
(
	{
		question:"filename of question", correct:"the correct option to be retrieved from the sensor package"
		on_wrong:"filename of audio to play if user chooses wrong option to question", 
		return_on_wrong:"integer specifying question to return to if user chooses wrong option to question",
		on_correct:"filename of audio to play if user chooses right option to question",
		return_on_correct:"integer of quesiton to return to if the user chooses the correct option"
	}
)
ls = [{"name":"Nwafor", "filename":"name of file"}, {"name":"Livinus", "filename":"another file name"}]
"""
from speech_control import SoundControl as sc #importing the module we have programmed to take care of sound
import json


class Quiz(object):
	"""
	This class creates the instance for the quiz, a file is to be provided which has the record of all the audio files for each of the questions in the quiz
	and also the they correct option.
	"""
	def __init__(self, file):
		with open(file, 'r') as f:
			data = f.read()
		self.questions = json.loads(data)
		for q in self.questions:
			q["question"] = sc(q["question"]) #reconfiguring the question to a sound control object
			if not q.get("on_wrong") == None: #making sure that the on_wrong option is not set to None befor setting it be a sound control object
				q["on_wrong"] = sc(q["on_wrong"])
			if not q.get("on_correct") == None: #making sure that the on_correct option is not set to None befor setting it to be a sound control object
				q["on_correct"] = sc(q["on_correct"])

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
		"""
		q["question"].play(True) #playing the question
		choice = self.get_user_choice() #getting the user's choice
		if choice == q["correct"]: #checking if choice is correct
			if q.get('on_correct') is not None:
				q['on_correct'].play(True)
			if q.get('return_on_correct') is not None:
				self.play_question(q['return_on_correct'])
		elif q.get('return_on_wrong') is not None: #in case choice is not correct
			if q.get('on_wrong') is not None:
				q['on_wrong'].play(True)
			self.play_question(q['return_on_wrong'])
		else:
			if q.get('on_wrong') is not None:
				q['on_wrong'].play(True)

	def get_user_choice(self):
		"""
		This method is meant to exam the package and get the users response
		"""
		response = input("Type your answer:  ")
		return response

	def take_quiz(self):
		"""
		This takes care of the quiz
		"""
		for q in self.questions: #iterating through the questions
			self.play_question(q)

