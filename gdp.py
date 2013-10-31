'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from devices import *
from formats import *
from tools import *


def main():
	device   = DeviceAtmelStudio(part="atmega32u4")
	tool     = ToolAtmelAVRISPMKII(device, port=None, interface="isp")

	tool.open(250000)


if __name__ == "__main__":
    main()
