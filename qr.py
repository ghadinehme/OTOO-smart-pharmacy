import requests
# from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
import serial

def read_qr():
    serial_port = '/dev/cu.usbserial-14120'

    baud_rate = 9600

    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    url = ''

    while len(url) == 0:
        url = ser.readline().decode().strip()

    # Make an HTTP request to the URL and extract the text content from the response
    response = requests.get(url)
    html_content = str(response.content)
    if 'Skip advertisement' in html_content:
        ind = str(response.content).index("https://me-qr.com/text/")
        url = str(response.content)[ind:ind+35]
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text().strip()
        print(text.split("\n")[-1])
        return text.split("\n")[-1]
    else:
        print(f"Failed to retrieve contents from URL {url}. Status code: {response.status_code}")

# read_qr()