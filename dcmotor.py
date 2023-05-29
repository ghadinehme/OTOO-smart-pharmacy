import RPi.GPIO as GPIO
import time
relay_pin = 3
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

GPIO.output(relay_pin, GPIO.HIGH)

GPIO.cleanup()
