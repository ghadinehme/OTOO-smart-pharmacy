import RPi.GPIO as GPIO
import time



def dispense(request):
	# import all ender functions
	
	# Set the GPIO mode
	GPIO.setmode(GPIO.BCM)
	BEAM_PIN = 27

	def break_beam_callback(channel):
		if GPIO.input(BEAM_PIN):
			print("beam unbroken")
		else:
			print("beam broken")

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=break_beam_callback)
	

	relay_pin = 4
		
	# Set up the GPIO pins
	GPIO.setup(relay_pin, GPIO.OUT)
	GPIO.output(relay_pin, GPIO.HIGH)
	count = 0
	
	old = 0

	while count < request:
		if GPIO.input(BEAM_PIN):
			old = 0
			print("beam unbroken")
		else:
			if old == 0:
				count += 1
				old = 1
			print("beam broken")
		print(count)
		
		
	GPIO.output(relay_pin, GPIO.LOW)
		

	GPIO.cleanup()

if __name__ == '__main__':
	dispense(1)
