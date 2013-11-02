'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class Device(object):
	def __init__(self):
		raise NotImplementedError


	def get_name(self):
		raise NotImplementedError


	def get_vcc_range(self):
		raise NotImplementedError


	def get_supported_interfaces(self):
		raise NotImplementedError


	def get_param(self, group, param):
		raise NotImplementedError


	def get_signature(self, interface):
		raise NotImplementedError
