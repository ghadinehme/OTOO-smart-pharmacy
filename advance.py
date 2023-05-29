import RPi.GPIO as GPIO
import time
import serial
import logging



def dispense(request, location):
	# Ender Starters 
	
	serial_port = '/dev/ttyUSB1'
	baud_rate = 115200

	ser = serial.Serial(serial_port, baud_rate, timeout=1)

	logging.basicConfig(filename='printer.log', level=logging.INFO)

	# Ender Functions
	
	def get_printer_status(ser):
		try:
			ser.write(b'M119\n')
			response = ser.readline().decode('utf-8').strip()
			if 'Error:' in response:
				logging.error(response)
			else:
				status = parse_status(response)
				logging.info('Printer status: ' + str(status))
				return status
		except serial.SerialException as e:
			logging.error('Error: ' + str(e))

	def parse_status(response):
		status = {}
		lines = response.split("\n")
		for line in lines:
			if line.startswith("X:"):
				status["x_position"] = float(line.split(":")[1].strip())
		return status


	def move_to_home_position(ser):
		try:
			ser.write(b'G28\n')
			max_iterations = 10
			iteration_count = 0
			x_position = y_position = z_position = None 
			while True:
				time.sleep(0.1)
				print('Waiting for response...')
				response = ser.readline().decode('utf-8').strip()
				print('Got response:', response)
				if 'X:' in response and 'Y:' in response and 'Z:' in response:
					x_position = float(response.split('X:')[1].split()[0])
					y_position = float(response.split('Y:')[1].split()[0])
					z_position = float(response.split('Z:')[1].split()[0])
					if x_position < 1 and y_position < 1 and z_position < 1:
						break
				iteration_count += 1
				if iteration_count >= max_iterations:
					logging.error('Error: Timed out waiting for printer to move to home position')
					break
				time.sleep(0.1)
			logging.info('Moved to home position. X position: ' + str(x_position) + ', Y position: ' + str(y_position) + ', Z position: ' + str(z_position))
		except serial.SerialException as e:
			logging.error('Error: ' + str(e))

	def move_to_medication_position(ser, medication_number):
		try:
			medication_positions = {
				1: 5,
				2: 200,
				3: 300,
				4: 400,
				5: 500,
				6: 600,
				7: 700,
				8: 800
			}
			if medication_number not in medication_positions:
				logging.error('Error: Invalid medication number')
				return
			time.sleep(1)    
			gcode = f'G1 X {medication_positions[medication_number]}\n'
			ser.write(gcode.encode())
			max_iterations = 10
			iteration_count = 0
			x_position = None
			while True:
				time.sleep(0.5)
				print('Waiting for response...')
				response = ser.readline().decode('utf-8').strip()
				print('Got response:', response)
				if 'X:' in response:
					x_position = float(response.split('X:')[1].split()[0])
				if x_position == medication_positions[medication_number]:
					break
				iteration_count += 1
				if iteration_count >= max_iterations:
					logging.error(f'Error: Timed out waiting for printer to move to medication position {medication_number}')
					break
			logging.info(f'Moved to medication position {medication_number}. X position: ' + str(x_position))
			return x_position
		except serial.SerialException as e:
			logging.error('Error: ' + str(e))


	def openlog():
		with open('printer.log', 'r') as f:
			print(f.read())

	def clearlog():
		with open('printer.log', "w") as f:
			f.write("")
			
	######################################################################
	############################## End of Ender Functions ################
	######################################################################
	
 
	# Set the GPIO mode
	GPIO.setmode(GPIO.BCM)
	BEAM_PIN = 27
	enable_pin_disp = 18
	
	# Define the GPIO pins connected to the MDD10A inputs
	motor1_in1 = 23
	enable_pin = 24
	
	# Set the GPIO pins as outputs
	GPIO.setup(motor1_in1, GPIO.OUT)
	GPIO.setup(enable_pin, GPIO.OUT)

	pwm = GPIO.PWM(enable_pin, 100)
	

	# Set the GPIO pins as outputs
	GPIO.setup(motor1_in1, GPIO.OUT)
	GPIO.setup(enable_pin, GPIO.OUT)
	
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
	
	# Move to Location
	#TODO
	
	# Open Blade
	motor_forward(70)
	time.sleep(0.2)
	motor_stop()
	
	        
	move_to_home_position(ser)
	move_to_medication_position(ser, location)
	
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
	#GPIO.setup(enable_pin_disp, GPIO.OUT)
	#pwmDisp = GPIO.PWM(enable_pin_disp, 100)
	
	GPIO.output(relay_pin, GPIO.HIGH)
	count = 0
	#pwmDisp.start(100)
	
	old = 1

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
		
	#pwmDisp.stop()
	
	GPIO.output(relay_pin, GPIO.LOW)
	
	#Slice Blade
	time.sleep(0.5)
	motor_backward(100)
	time.sleep(0.6)  # Run the motor forward for 2 seconds
	motor_stop()
	
	time.sleep(1)        
	move_to_home_position(ser)
		

	GPIO.cleanup()
	
		

if __name__ == '__main__':
	a = input("Choose the number of pills:")
	dispense(int(a))
