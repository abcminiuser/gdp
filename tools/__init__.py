'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool import *
from tools.tool_atmel_avrisp import *
from tools.tool_atmel_avrispmkii import *
from tools.tool_atmel_jtagicemkii import *
from tools.tool_atmel_stk500 import *

gdp_tools = \
	{
		'avrisp'		:	ToolAtmelAVRISP,
		'avrispmkii'	:	ToolAtmelAVRISPMKII,
		'jtagicemkii'	:	ToolAtmelJTAGICEMKII,
		'stk500'		:	ToolAtmelSTK500
	}
