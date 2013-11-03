'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
try:
	import serial
except ImportError:
	print("The PySerial library is not installed.")
	sys.exit(1)

from transports import *


class TransportSerial(Transport):
	def __init__(self, port=None, baud=115200):
		self.dev_handle = None
		self.port = port
		self.baud = baud


	def open(self):
		if self.port is None or self.baud is None:
			raise TransportError("Transport serial port or baudrate are not set.")

		try:
			self.dev_handle = serial.Serial(port=self.port, baudrate=self.baud, timeout=.5, interCharTimeout=.05)
		except:
			raise TransportError("Specified serial port could not be opened.")


	def close(self):
		if dev_handle is not None:
			dev_handle.flush()
			dev_handle.close()


	def read(self):
		return [ord(x) for x in self.dev_handle.read(1000)]


	def write(self, data):
		self.dev_handle.write(''.join([chr(c) for c in data]))
