
import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

relay_pin = 4
	
# Set up the GPIO pins
GPIO.setup(relay_pin, GPIO.OUT)

request = 2  # Number of times to break the beam
count = 0  # Counter for the number of times beam is broken
GPIO.output(relay_pin, GPIO.HIGH)
time.sleep(1)


while count < request:
	# Turn on the relay module
	GPIO.output(relay_pin, GPIO.HIGH)

	# Wait for Approproate Time (seconds)
	time.sleep(1)

	# Turn off the relay module
	GPIO.output(relay_pin, GPIO.LOW)
	
	# Wait for Approproate Time (seconds)
	time.sleep(0.1)
	count += 1
	

GPIO.cleanup()
