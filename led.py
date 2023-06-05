import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_LIGHTS = [25,12,16,26]

for i in LED_LIGHTS:
    GPIO.setup(i, GPIO.OUT)

def turn_on_led(i):
    GPIO.output(LED_LIGHTS[i], GPIO.HIGH)
    print("LED turned on")

def turn_off_led(i):
    GPIO.output(LED_LIGHTS[i], GPIO.LOW)
    print("LED turned off")
    
def turn_off_leds():
	for light in LED_LIGHTS:
		GPIO.output(light, GPIO.LOW)
		print("LED turned off")

if __name__ == "__main__":
	turn_on_led(1)
