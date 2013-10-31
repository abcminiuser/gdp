'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class Tool(object):
	def __init__(self):
		raise NotImplementedError


	def get_name(self):
		raise NotImplementedError


	def get_supported_interfaces(self):
		raise NotImplementedError


	def open(self, target_frequency):
		raise NotImplementedError


	def close(self):
		raise NotImplementedError


	def read(self):
		raise NotImplementedError


	def write(self, data):
		raise NotImplementedError
