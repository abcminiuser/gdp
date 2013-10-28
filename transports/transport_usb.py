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

		dev_handle = usb.core.find(idVendor=self.vid, idProduct=self.pid)
		if dev_handle is None:
			return False

		dev_handle.set_configuration()
		return True

	def close(self):
		pass
