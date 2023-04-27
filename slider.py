import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

wired_pins = [23, 24]

def slider_turn(destination, direction):
	# Set the GPIO mode
	GPIO.setmode(GPIO.BCM)

	dir_pin = 24
	go_pin = 23
	switch_pin = 6
	
	# Set up the GPIO pins
	GPIO.setup(go_pin, GPIO.OUT)
	GPIO.setup(dir_pin, GPIO.OUT)
	GPIO.setup(switch_pin, GPIO.IN)

	# Turn on the relay module
	if direction == 0:
		GPIO.output(dir_pin, GPIO.LOW)
		GPIO.output(go_pin, GPIO.HIGH)
		# Wait for Approproate Time (seconds)
		duration = dest_to_time(destination, direction)
		time.sleep(duration)
	else:
		GPIO.output(dir_pin, GPIO.HIGH)
		GPIO.output(go_pin, GPIO.HIGH)
		while GPIO.input(switch_pin):
			boo = True
	

	# Wait for Approproate Time (seconds)
	#duration = dest_to_time(destination, direction)
	#time.sleep(duration)

	# Turn off the relay module
	GPIO.output(go_pin, GPIO.LOW)
	GPIO.output(dir_pin, GPIO.LOW)

	# Clean up the GPIO pins
	GPIO.cleanup()
	
def dest_to_time(destination, direction):
	times = [30, 17, 5]
	error = [1.3, 0.9, 0.3]
	return times[destination - 1] + direction*error[destination - 1]
	
	
if __name__ == '__main__':
	#slider_turn(1, 0)
	time.sleep(2)
	slider_turn(1, 1)
