'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class Protocol(object):
	def __init__(self):
		raise NotImplementedError


	def open(self, target_frequency):
		raise NotImplementedError


	def close(self):
		raise NotImplementedError
