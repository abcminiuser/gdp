GDP - The Generic Device Programmer
===================================

What is it?
---------------------

GDP is aimed to be an eventual alternative programmer front-end similar to the
ATPROGRAM tool from Atmel, but cross-platform, open-source and supporting third
party tools. It aims to lower the barrier to entry to adding new device, tool
protocol and transport support, with a consistent front-end interface.


What about AVRDUDE?
---------------------

AVRDude, an alternative project similar to GDP and ATPROGRAM is already
available and widely used. However, it is written in C which discourages some
people from contributing, and uses its own internal device and tool
configuration files. GDP aims at supporting multiple device back-ends, including
the raw device XML files pulled from Atmel Studio.


Project Status
---------------------

It's a new project, so don't expect functional *anything* right now. Fork, poke,
pull-request if you're interested, otherwise just sit back and wait for a public
beta release.


Support
---------------------

The project support is listed below.


Device Definitions:

+ Atmel AVR Studio Device XML


Tools:

+ Atmel AVR109 Bootloader
+ Atmel AVR8 DFU Bootloader
+ Atmel STK500
+ Atmel STK600
+ Atmel AVRISP
+ Atmel AVRISP-MKII
+ Atmel JTAG-ICE MKII
+ Atmel Dragon


Protocols:

+ Atmel AVR109 Protocol
+ Atmel DFUV1 Protocol
+ Atmel STKV2 Protocol (ISP, HVSP, HVPP, PDI, TPI and XMEGA JTAG interfaces only)
+ Atmel JTAGV2 Protocol (Stub only, no implementation)


Transports:

+ Atmel Jungo USB Transport
+ Atmel AVR8 DFU Transport
+ Serial Transport


Input File Formats:

+ Intel HEX (HEX, EEP)
+ Binary (BIN)
+ Executable and Linkable Format (ELF)


Output File Formats:

+ Intel HEX (HEX, EEP)
+ Binary (BIN)


User Interfaces:

+ CLI (PROGRAM, READ, VERIFY, CHIPERASE, ERASE and LIST commands)


USB Drivers
---------------------

As proprietary USB drivers are difficult to interface with (for both technical
and legal reasons) all USB transports use LibUSB as the driver backend. This
means that USB tools must have LibUSB drivers (or the LibUSB filter driver)
installed instead of their regular Jungo or other proprietary driver for GDP to
be able to communicate with them.


Prerequisites
---------------------

The following is required to use GDP currently in its original Python form:

+ Python 2.7
+ PyUSB Library
+ PySerial Library
+ PyELFTools Library
+ IntelHex Library

If compiled with the PyInstaller toolkit, the above is not required as all
dependencies are converted into a native platform executable.

In addition, the device files from Atmel Studio are required for the current
device backend.


Contact
---------------------

Source Code:    http://github.com/abcminiuser/gdp

Author's Site:  http://www.fourwalledcubicle.com

Author's Email: dean [at] fourwalledcubicle [dot] com
