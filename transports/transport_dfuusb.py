'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
try:
	import usb.core
	import usb.util
except ImportError:
	print("The PyUSB library is not installed.")
	sys.exit(1)

from transports import *


class TransportDFUUSB(Transport):
	DFU_REQUEST_DNLOAD = 1
	DFU_REQUEST_UPLOAD = 2


	def __init__(self, vid=0x03eb, pid=None):
		self.dev_handle = None
		self.vid = vid
		self.pid = pid

		self.sequence = 0


	def open(self):
		if self.vid is None or self.pid is None:
			raise TransportError("Transport VID or PID are not set.")

		self.dev_handle = usb.core.find(idVendor=self.vid, idProduct=self.pid)
		if self.dev_handle is None:
			raise TransportError("Specified tool was not found on the USB bus.")

		self.dev_handle.set_configuration()


	def close(self):
		pass


	def read(self, request, length):
		bmRequestType = usb.util.build_request_type(
                        usb.util.CTRL_IN,
                        usb.util.CTRL_TYPE_CLASS,
                        usb.util.CTRL_RECIPIENT_INTERFACE
                    )

		if request == TransportDFUUSB.DFU_REQUEST_UPLOAD:
			value = self.sequence
			self.sequence += 1
		else:
			value = 0

		return self.dev_handle.ctrl_transfer(bmRequestType=bmRequestType,
		                                     bRequest=request,
		                                     wValue=value,
		                                     wIndex=0,
		                                     data_or_wLength=length,
		                                     timeout=5000)


	def write(self, request, data):
		bmRequestType = usb.util.build_request_type(
                        usb.util.CTRL_OUT,
                        usb.util.CTRL_TYPE_CLASS,
                        usb.util.CTRL_RECIPIENT_INTERFACE
                    )

		if request == TransportDFUUSB.DFU_REQUEST_DNLOAD:
			value = self.sequence
			self.sequence += 1
		else:
			value = 0

		self.dev_handle.ctrl_transfer(bmRequestType=bmRequestType,
		                              bRequest=request,
		                              wValue=value,
		                              wIndex=0,
		                              data_or_wLength=data,
		                              timeout=5000)
