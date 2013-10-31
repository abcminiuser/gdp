'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from devices import *
from formats import *
from tools import *


def main():
	device   = DeviceAtmelStudio(part="atxmega256a3bu")
	tool     = ToolAtmelAVRISPMKII(device, port=None, interface="isp")

	tool.open()


if __name__ == "__main__":
    main()
