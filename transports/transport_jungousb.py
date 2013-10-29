'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import usb.core
import usb.util
from transports import *


class TransportJungoUSB(Transport):
	dev_handle = None
	vid = None
	pid = None
	read_ep = None
	write_ep = None


	def __init__(self, vid, pid, read_ep, write_ep):
		self.vid = vid
		self.pid = pid
		self.read_ep = read_ep
		self.write_ep = write_ep


	def open(self):
		if (self.vid is None or self.pid is None):
			raise ValueError("Tool VID or PID are not set.")

		if (self.read_ep is None or self.write_ep is None):
			raise ValueError("Tool Read or Write Endpoint indexes are not set.")

		self.dev_handle = usb.core.find(idVendor=self.vid, idProduct=self.pid)
		if self.dev_handle is None:
			return False

		self.dev_handle.set_configuration()
		return True


	def close(self):
		pass


	def read(self):
		data = []

		while len(data) % 64 == 0:
			data.extend(self.dev_handle.read(usb.util.ENDPOINT_IN | self.read_ep, 64, 0, 1000))

		return data


	def write(self, data):
		self.dev_handle.write(usb.util.ENDPOINT_OUT | self.write_ep, data, 0, 1000)
