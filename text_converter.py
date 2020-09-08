try:#trying to import required module
	import pyttsx3 as pyt
except:
	try:
		import pip
		pip.main(['pyttsx3'])#trying to install required module
		#module can now be imported since it has been installed

		import pyttsx3 as pyt
	except:
		print("Problem installing pyttsx3 module, check your internet connection and try again or run the command 'pip install pyttsx3' on your command line interface")

# engine = pyt.init()
# engine.say('Hello how are you doing at the moment?')
# engine.runAndWait()

class Converter:
	"""
	This class takes care of initializing a pyttsx3 text to speech converter engine and creating an event loop to work with the converter
	"""
	def __init__(self, opening_speech=False):
		self.engine = pyt.init()
		if not opening_speech == False:
			self.say(opening_speech)#spelling out the opening speech


	def say(self, text):
		self.engine.say(text)
		self.engine.runAndWait()

	def select_voice(self):
		current_voice_id = self.engine.getProperty('voice')
		for voice in self.engine.getProperty('voices'):
			self.engine.setProperty('voice', voice.id)#setting the voice
			self.say("Do you want to select my voice?")#asking if user want this voice
			response = input('type "yes" to select this voice and "no" to skip :')#collecting user's response
			if response == 'yes':# checking if the user selected the voice
				current_voice_id = voice.id#setting that the current voice id is this voice id
				break
		self.engine.setProperty('voice', current_voice_id)#setting that the voice is the current_voice_id variable which holds the selected voice id	

speech = Converter("You can now tell me anything that pleases you")
speech.select_voice()
speech.say('thank you for selecting my voice')