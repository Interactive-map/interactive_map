import serial
import time
arduino = serial.Serial('/dev/ttyUSB0', 9600)

while True:
	print(arduino.readline())
	time.sleep(.5)
