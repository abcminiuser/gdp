'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool import *
from tools.tool_atmel_avrispmkii import *
from tools.tool_atmel_jtagicemkii import *

gdp_tools = \
	{
		'avrispmkii'	:	ToolAtmelAVRISPMKII,
		'jtagicemkii'	:	ToolAtmelJTAGICEMKII
	}
