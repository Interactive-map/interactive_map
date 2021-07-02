from speech_control import SoundControl as sc #importing the module that have been programmed to take care of sound
from text_converter import Converter as ct #importing the module that have been programmed to convert text to speech
from sensor import Sensor
from quiz import Quiz
from lesson import Lesson
from platform import system #importing method to be used to check the system that the program is running from

data2 = {
	"Africa":{'2'},
	"Antarctica":{'11'},
	"Asia":{'4'},
	"Australia":{'7'},
	"Europe":{'3'},
	"South America":{'0'},
	"North America":{'1'}
}
com_port = "COM13"
if not system() == "Windows":#checking if the current operating system is not windows so as to change syntax for specifying the serial communication port
	com_port = '/dev/ttyUSB0'
board = Sensor(data2, com_port, 9600)
lesson = Lesson("lesson_files/map_of_continents_lesson_recorded_format.txt")
# source -- https://www.indiatoday.in/education-today/gk-current-affairs/story/7-continents-of-the-world-facts-html-1334565-2018-09-07
# https://www.kids-world-travel-guide.com/continent-facts.html#:~:text=There%20are%20seven%20continents%20and,the%20waters%20of%20the%20oceans.&text=The%20seven%20continents%20on%20our,South%20America%20and%20Oceania%2FAustralia.
# https://en.wikipedia.org/wiki/Continent
lesson.configure_with_sound_control() # specifying that the voicing should be recorded sound

quiz = Quiz("quiz_files/map_of_continents_quiz_recorded_format.txt")
quiz.configure_with_sound_control() # specifying that the voicing should be recorded sound

lesson.quiz = quiz#setting the quiz for the lesson
quiz.lesson = lesson#setting the lesson for the quiz
lesson.board = board#setting the arduino board for the lesson 
quiz.board = board#setting the arduino board for the quiz

while True:
	lesson.take_lesson()#starting with lesson mode