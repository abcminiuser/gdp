'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import serial
from transports import *


class TransportSerial(Transport):
	dev_handle = None
	port = None
	baud = None


	def __init__(self, port=None, baud=115200):
		self.port = port
		self.baud = baud


	def open(self):
		if self.port is None or self.baud is None:
			raise ValueError("Transport serial port or baudrate are not set.")

		self.dev_handle = serial.Serial(port=self.port, baudrate=self.baud, timeout=.5, interCharTimeout=.05)
		return True


	def close(self):
		if dev_handle is not None:
			dev_handle.flush()
			dev_handle.close()


	def read(self):
		return self.dev_handle.read(1000)


	def write(self, data):
		self.dev_handle.write(data)
