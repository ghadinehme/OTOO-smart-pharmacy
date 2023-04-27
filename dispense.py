import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

wired_pins = [17, 27, 22]

def motor_turn(pos, quantity):
	# Set the GPIO mode
	GPIO.setmode(GPIO.BCM)

	wired_pins = [17, 27, 22]

	# Set the GPIO pins for the relay module
	relay_pin = wired_pins[pos - 1]
	
	# Set up the GPIO pins
	GPIO.setup(relay_pin, GPIO.OUT)
	
	duration = quantity_to_time(quantity)
	
	real_dur = 0
	
	while real_dur < duration:
		# Turn on the relay module
		#GPIO.output(relay_pin, GPIO.HIGH)

		# Wait for Approproate Time (seconds)
		#time.sleep(2)

		# Turn off the relay module
		#GPIO.output(relay_pin, GPIO.LOW)
		
		# Wait for Approproate Time (seconds)
		#time.sleep(0.1)
		
		# Turn on the relay module
		GPIO.output(relay_pin, GPIO.HIGH)

		# Wait for Approproate Time (seconds)
		time.sleep(0.5)

		# Turn off the relay module
		GPIO.output(relay_pin, GPIO.LOW)
		
		# Wait for Approproate Time (seconds)
		time.sleep(0.1)
		
		real_dur += 0.6
		

	# Clean up the GPIO pins
	GPIO.cleanup()
		
	
def quantity_to_time(quantity):
	return quantity * 3
	
if __name__ == '__main__':
	motor_turn(1, 6)
