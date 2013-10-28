'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool_avrispmkii import *

def main():
	currtool = ToolAVRISPMKII()
	currtool.open()
	currtool.close()


if __name__ == "__main__":
    main()
