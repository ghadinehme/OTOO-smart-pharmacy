import RPi.GPIO as GPIO
import time



def cut():
	# Set the GPIO mode
	GPIO.setmode(GPIO.BCM)
	
	relay_pin = 20
	relay_pin_power = 22
	relay_pin2 = 26
		
	# Set up the GPIO pins
	GPIO.setup(relay_pin, GPIO.OUT)
	GPIO.setup(relay_pin2, GPIO.OUT)
	GPIO.setup(relay_pin_power, GPIO.OUT)
	
	GPIO.output(relay_pin_power, GPIO.HIGH)
	
		
	GPIO.output(relay_pin, GPIO.LOW)
	GPIO.output(relay_pin2, GPIO.HIGH)
	time.sleep(0.3)
	
	GPIO.output(relay_pin, GPIO.HIGH)
	GPIO.output(relay_pin2, GPIO.LOW)
	time.sleep(0.3)

	
	GPIO.output(relay_pin_power, GPIO.LOW)

	GPIO.cleanup()

if __name__ == '__main__':
	cut()
