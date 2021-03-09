from speech_control import SoundControl as sc #importing the module that have been programmed to take care of sound
from text_converter import Converter as ct #importing the module that have been programmed to convert text to speech
from sensor import Sensor
from quiz import Quiz
from lesson import Lesson
from platform import system #importing method to be used to check the system that the program is running from

data2 = {
	"Africa":{'2'},
	"Antactica":{'11'},
	"Asia":{'4'},
	"Australia":{'7'},
	"Europe":{'3'},
	"South America":{'0'},
	"North America":{'1'}
}
board = Sensor(data2, "COM13", 9600)
if not system() == "Windows":#checking if the current operating system is not windows so as to change syntax for specifying the serial communication port
	board = Sensor(data2, '/dev/ttyUSB0', 9600)

lesson = Lesson("lesson_files/map_of_continents_lesson.txt")
lesson.configure_with_tts_converter()

quiz = Quiz("quiz_files/map_of_continents_quiz.txt")
quiz.configure_with_tts_converter()

lesson.quiz = quiz#setting the quiz for the lesson
quiz.lesson = lesson#setting the lesson for the quiz
lesson.board = board#setting the arduino board for the lesson 
quiz.board = board#setting the arduino board for the quiz

while True:
	lesson.take_lesson()#starting with lesson mode