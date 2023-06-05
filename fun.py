import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_LIGHTS = [25,12,16,26]

for i in LED_LIGHTS:
    GPIO.setup(i, GPIO.OUT)

def turn_on_led(j):
    GPIO.output(j, GPIO.HIGH)
    print("LED turned on")

def turn_off_led(j):
    GPIO.output(j, GPIO.LOW)
    print("LED turned off")

try:
    while True:
        for i in LED_LIGHTS:
            if np.random.rand()<0.5:
                turn_on_led(i)
            else:
                turn_off_led(i)
        time.sleep(0.5)  # LED off for 1 second

except KeyboardInterrupt:
    for i in LED_LIGHTS:
        turn_off_led(i)
    print("Exiting...")
    GPIO.cleanup()
