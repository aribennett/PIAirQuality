import os
import sys
import glob
import serial
import struct
import dotenv
from time import time
from collections import namedtuple
from Adafruit_IO import Client

PAYLOAD_LENGTH = 10
PAYLOAD_STRUCT = '<BBHHHBB'
PAYLOAD_HEADERS = namedtuple('Reading', 'HDR CMD PM25 PM10 ID CHK TAIL')
MESSAGE_INTERVAL = 60

def parse_pmi(bytes):
    raw = list(struct.unpack(PAYLOAD_STRUCT, bytes))
    # rescale the readings
    raw[2] /= 10
    raw[3] /= 10
    output = PAYLOAD_HEADERS._make(raw)
    return output

if __name__ == "__main__":
    dotenv.load_dotenv()
    aio_client = Client(os.environ.get('ADAFRUIT_IO_USERNAME'), os.environ.get('ADAFRUIT_IO_KEY'))
    serial_device = serial.Serial(
        port=os.environ.get('SERIAL_DEVICE'),
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=.1,
    )

    input_str = b''
    last_message_time = 0
    while True:
        char = serial_device.read()
        if len(char):
            input_str += char
        elif len(input_str) == PAYLOAD_LENGTH:
            values = parse_pmi(input_str)
            print(values)
            if time() - last_message_time > MESSAGE_INTERVAL:
                try:
                    aio_client.send(os.environ.get('ADAFRUIT_IO_FEED'), values.PM25)
                    last_message_time = time()
                except Exception as e:
                    print(e)
            input_str = b''
        else:
            input_str = b''
