

"""
The purpose of this module is to control the sound input to the system and also the sound output to the system.
The methods defined in this module are working with respect to the imported moudles. So for safety reasons it will be better to import thess mpdule
before we proceed with the program
"""

try:
	import sounddevice as sd
	import soundfile as sf
except:
	try:
		import pip
		pip.main(['install', 'sounddevice', 'soundfile'])#trying to the installation of the modules required
		#now the packages can now be installed as their have been installed
		import soundfile as sf
		import sounddevice as sd
	except:
		print("check your internet connection and try again, packages are missing and pip is unable to install the required packages")


class SoundControl(object):
	def __init__(self, soundfile):
		"""
		The user is expected to provide the soundfile to be controlled
		"""
		self.soundfile = soundfile
		self.make_sound()
	def make_sound(self):
		"""
		this method makes the sound to be played
		"""
		self.sound_data, self.sound_rate = sf.read(self.soundfile, dtype="float32")


	def play(self, wait=False):
		"""
		This method plays the sound
		"""
		sd.play(self.sound_data, self.sound_rate)
		#the parameter wait defines if the sound should play completely before any other program is run or not
		if wait:
			sd.wait()

	def wait(self):
		"""
		waits until the sound is done playing
		"""
		sd.wait()

