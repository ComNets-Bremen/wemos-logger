# Install the pycom firmware

In the [previous manual step](hardware.md), you have assembled the hardware. Next, the firmware has to be programmed to the device. In this example, we will use Python or more specifically micropython (-> [micropython.org](http://micropython.org/). This is a python interpreter for microcontrollers. The installation is described in detail on the [webpage](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#deploying-the-firmware). For the wemos device, the corresponding firmware files can be found [here](https://micropython.org/download/esp8266/). You need the stable version for 2M or more flash. While writing this document, version 1.15 is the most recent one: `esp8266-20210418-v1.15.bin`


## Quick walk through: Installing the firmware:

We are using a virtual environment to install all packages locally and not system wide as they are only required for the firmware update and not for the daily work (c.f. [Python3 documentation](https://docs.python.org/3/library/venv.html)). The examples are taken from a Linux system but will also work on Windows and MacOS with only minor changes. Please be aware that the serial port of the device has to be changed according to your system. Here, `/dev/ttyUSB0` is used. On a Windows machine, this might be `COM3` or similar.

The basic steps are as follows and executed on the command line:

* Create a virtual environment: `python3 -m venv venv`
* Activate the virtual envoironment: `. ./venv/bin/activate`. You will now see the name of your virtual environment in front of the command line.
* Install the esptool: `pip3 install esptool`
* Connect the wemos device via USB
* Erase the flash: `esptool.py --port /dev/ttyUSB0 erase_flash`
* Upload the firmware you have downloaded from micropython.org: `esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20210418-v1.15.bin`

After these steps, the firmware is successfully installed. This usually only has to be done once per device.

Please be aware that the commands are slightly different for Windows systems:
`.\venv\Scripts\activate`
