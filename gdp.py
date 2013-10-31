'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from devices import *
from formats import *
from tools import *


def test_program(device, tool):
	protocol = tool.get_protocol()

	tool.open()

	device_vtarget = protocol.get_vtarget()
	dev_vccrange = device.get_vcc_range()
	if not dev_vccrange[0] <= device_vtarget <= dev_vccrange[1]:
		raise ValueError("Device VCC range of (%0.2fV-%0.2fV) is outside "
		                 "the measured VTARGET of %0.2fV." %
		                 (dev_vccrange[0], dev_vccrange[1], measured_vtarget))

	protocol.set_interface_frequency(250000)

	tool.close()


def main():
	device   = DeviceAtmelStudio(part="atmega32u4")
	tool     = ToolAtmelAVRISPMKII(device, port=None, interface="isp")

	test_program(device, tool)



if __name__ == "__main__":
    main()
