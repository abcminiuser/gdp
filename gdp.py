'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
from optparse import OptionParser, OptionGroup

from devices import *
from formats import *
from tools import *


def gdp(options, args):
	try:
		device = DeviceAtmelStudio(part=options.device)
	except:
		print("ERROR: Unknown device \"%s\"." % options.device)
		sys.exit(1)

	try:
		tool = gdp_tools[options.tool](device, port=options.port, interface=options.interface)
	except KeyError:
		print("ERROR: Unknown tool \"%s\". Known tools are:" % options.tool)

		for key, value in gdp_tools.iteritems() :
		    print("  - %s (%s)" % (key, gdp_tools[key].get_name()))

		sys.exit(1)
	except LookupError as message:
		print("ERROR: %s" % message)
		sys.exit(1)


	protocol = tool.get_protocol()

	try:
		tool.open()

		if not options.no_verify_vtarget:
			device_vtarget = protocol.get_vtarget()
			dev_vccrange = device.get_vcc_range()

			if not dev_vccrange[0] <= device_vtarget <= dev_vccrange[1]:
				raise ValueError("Device VCC range of (%0.2fV-%0.2fV) is outside "
				                 "the measured VTARGET of %0.2fV." %
				                 (dev_vccrange[0], dev_vccrange[1], device_vtarget))

		protocol.set_interface_frequency(options.frequency)
		protocol.enter_session()

		protocol.exit_session()
		tool.close()
	except (ValueError, LookupError, IOError) as message:
		print("ERROR: %s" % message)


def main():
	description = "GDP, the Generic Device Programmer."
	usage = "usage: %prog [options] FILE"

	parser = OptionParser(usage=usage, description=description)

	comm_group = OptionGroup(parser,
	                         "Communication Settings",
	                         "Basic device/tool settings.")
	comm_group.add_option("-d", "--device",
	                  action="store", type="string", dest="device",
	                  help="target device selection")
	comm_group.add_option("-t", "--tool",
	                  action="store", type="string", dest="tool",
	                  help="target device selection")
	comm_group.add_option("-p", "--port",
	                  action="store", type="string", dest="port",
	                  help="communication port (for serial tools)")
	comm_group.add_option("-i", "--interface",
	                  action="store", type="string", dest="interface",
	                  help="communication interface to use to the target")
	comm_group.add_option("-f", "--frequency",
	                  action="store", type="int", dest="frequency", default=250000,
	                  help="communication interface frequency to use to the target")

	override_group = OptionGroup(parser,
	                             "Sanity Check Overrides",
	                             "[Here be dragons.]")
	override_group.add_option("", "--no-vtarget",
	                  action="store_true", dest="no_verify_vtarget",
	                  help="disable VCC range validity check of the target")

	parser.add_option_group(comm_group)
	parser.add_option_group(override_group)
	(options, args) = parser.parse_args()

	if options.device is None:
		print("ERROR: No device specified.")
		sys.exit(1)

	if options.tool is None:
		print("ERROR: No tool specified.")
		sys.exit(1)

	if options.interface is None:
		print("ERROR: No interface specified.")
		sys.exit(1)

	gdp(options, args)


if __name__ == "__main__":
    main()
