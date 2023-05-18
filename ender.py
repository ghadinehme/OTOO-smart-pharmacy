import serial
import logging
import time

serial_port = '/dev/ttyUSB0'
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate, timeout=1)

logging.basicConfig(filename='printer.log', level=logging.INFO)

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
            1: 100,
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

time.sleep(2)        
move_to_home_position(ser)
move_to_medication_position(ser,1)
