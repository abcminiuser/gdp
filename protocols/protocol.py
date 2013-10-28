'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class Protocol(object):
	def open(self):
		raise NotImplementedError

	def close(self):
		raise NotImplementedError
