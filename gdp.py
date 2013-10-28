'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool_avrispmkii import *
from protocols.protocol_atmelv2 import *

def main():
	tool     = ToolAVRISPMKII()
	protocol = ProtocolAtmelV2(tool)

	protocol.open()

if __name__ == "__main__":
    main()
