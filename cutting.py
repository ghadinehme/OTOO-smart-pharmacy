import RPi.GPIO as GPIO
import time

def setup():
	# Set GPIO pin numbering mode
	GPIO.setmode(GPIO.BCM)

	# Define the GPIO pins connected to the MDD10A inputs
	motor1_in1 = 23
	enable_pin = 24

	# Set the GPIO pins as outputs
	GPIO.setup(motor1_in1, GPIO.OUT)
	GPIO.setup(enable_pin, GPIO.OUT)

	pwm = GPIO.PWM(enable_pin, 100)

# Define motor control functions
def motor_forward(speed):
	GPIO.output(motor1_in1, GPIO.HIGH)
	#GPIO.output(motor1_in2, GPIO.HIGH)
	pwm.start(speed)

def motor_backward(speed):
	GPIO.output(motor1_in1, GPIO.LOW)
	#GPIO.output(motor1_in2, GPIO.HIGH)
	pwm.start(speed)

def motor_stop():

	GPIO.output(motor1_in1, GPIO.LOW)
	#GPIO.output(motor1_in2, GPIO.LOW)
	pwm.stop()

#motor_forward(70)
#time.sleep(0.2)
#motor_stop()
#time.sleep(5)
#motor_backward(100)
#time.sleep(0.4)  # Run the motor forward for 2 seconds
#motor_stop()

# Cleanup GPIO
#GPIO.cleanup()
