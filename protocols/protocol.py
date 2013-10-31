'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class Protocol(object):
	def __init__(self):
		raise NotImplementedError


	def get_vtarget(self):
		raise NotImplementedError


	def set_interface_frequency(self, target_frequency):
		raise NotImplementedError


	def open(self):
		raise NotImplementedError


	def close(self):
		raise NotImplementedError
