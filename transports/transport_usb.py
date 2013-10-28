'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import usb.core
import usb.util
from transports.transport import *

class TransportUSB(Transport):
	dev_handle = None
	vid = None
	pid = None


	def __init__(self, vid, pid):
		self.vid = vid
		self.pid = pid


	def open(self):
		if (self.vid is None or self.pid is None):
			raise ValueError("Tool VID or PID are not set.")

		self.dev_handle = usb.core.find(idVendor=self.vid, idProduct=self.pid)
		if self.dev_handle is None:
			return False

		self.dev_handle.set_configuration()
		return True


	def close(self):
		pass


	def read(self, endpoint, length, timeout):
		return self.dev_handle.read(usb.util.ENDPOINT_IN | endpoint, length, 0, timeout)


	def write(self, endpoint, data, timeout):
		self.dev_handle.write(usb.util.ENDPOINT_OUT | endpoint, data, 0, timeout)
