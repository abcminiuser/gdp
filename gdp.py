#!/usr/bin/env python

'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

import sys

from core import *


def main():
    interface = InterfaceCLI()
    sys.exit(interface.parse_arguments(sys.argv))


if __name__ == "__main__":
    main()
