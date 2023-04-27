import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)


# Define the pins for the DRV8825 motor controller
DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
EN = 16    # Enable GPIO Pin

# Set up the DRV8825 motor controller
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)
GPIO.output(DIR, GPIO.HIGH)
GPIO.output(EN, GPIO.LOW)

#TODO Define the number of steps required for each medication 

#360/1.8 = 200 steps for one full revolution of the motor (14HS13-0804S)

steps_for_med_1 = 400 # steps for the 14HS13-0804S to determine one full revolution
steps_for_med_2 = 400 
steps_for_med_3 = 600
direction = 0 
delay = 0.001

# Defining different motor movements for specified inputs by user, there are three corresponding to the three types of medications

def move_motor_med_one(steps_for_med_1):
    # Set the direction of movement
    GPIO.output(DIR, GPIO.HIGH)
    # Step the motor
    for i in range(steps_for_med_1):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

def move_motor_med_two(steps_for_med_2):
   # Set the direction of movement
    GPIO.output(DIR, GPIO.HIGH)
    # Step the motor
    for i in range(steps_for_med_2):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)


def move_motor_med_three(steps_for_med_3):
    # Set the direction of movement
    GPIO.output(DIR, GPIO.HIGH)
    # Step the motor
    for i in range(steps_for_med_3):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)


def back(steps_for_med_1):
    # Set the direction of movement
    GPIO.output(DIR, GPIO.LOW)
    # Step the motor
    for i in range(steps_for_med_1):
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)


# Creating IR break beam function to count pills 

def break_beam_callback(channel):
    if GPIO.input(BEAM_PIN):
        print("beam unbroken")
    else:
        print("beam broken")



def main():
    #back(steps_for_med_2)
    move_motor_med_one(steps_for_med_1)

if __name__ == "__main__":
   main()

