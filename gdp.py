'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from devices.device_atmelstudio import *
from tools.tool_avrispmkii import *
from tools.tool_jtagicemkii import *
from protocols.protocol_atmelv2 import *

def main():
	device   = DeviceAtmelStudio(part="atxmega256a3bu")
	tool     = ToolJTAGICEMKII()
	protocol = ProtocolAtmelV2(tool, device)

	protocol.open()

if __name__ == "__main__":
    main()
