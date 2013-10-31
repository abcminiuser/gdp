'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from devices import *
from formats import *
from protocols import *
from tools import *
from transports import *


def main():
	device   = DeviceAtmelStudio(part="atxmega256a3bu")
	tool     = ToolAtmelAVRISPMKII(port=None)
	protocol = ProtocolAtmelSTKV2(tool, device)

	protocol.open()


if __name__ == "__main__":
    main()
