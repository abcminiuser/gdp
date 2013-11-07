#!/usr/bin/env python

'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys

from core import *


def main():
    interface = InterfaceCLI()
    sys.exit(interface.parse(sys.argv))


if __name__ == "__main__":
    main()
