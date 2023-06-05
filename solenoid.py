import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

solenoid_pin = 21

GPIO.setup(solenoid_pin, GPIO.OUT)

def unlock():
    GPIO.output(solenoid_pin, GPIO.HIGH)
    print("Unlocked")

def lock():
    GPIO.output(solenoid_pin, GPIO.LOW)
    print("Locked")

if __name__ == "__main__":
    unlock()
    time.sleep(2)
    lock()
    time.sleep(2)
