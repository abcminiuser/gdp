'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from core.util import *
from tools.tool import *
from tools.tool_atmel_avr109 import *
from tools.tool_atmel_avr8dfu import *
from tools.tool_atmel_avrisp import *
from tools.tool_atmel_avrispmkii import *
from tools.tool_atmel_dragon import *
from tools.tool_atmel_jtagicemkii import *
from tools.tool_atmel_stk500 import *
from tools.tool_atmel_stk600 import *


def get_gdp_tool_aliases():
    aliases = dict()

    for t in Util.get_subclasses(Tool):
        aliases[t.get_name()] = t.get_aliases()

    return aliases


def get_gdp_tool(tool_alias):
    for t in Util.get_subclasses(Tool):
        if tool_alias in t.get_aliases():
            return t

    raise KeyError()
