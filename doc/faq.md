# FAQ / common problems

## The SD card is not recognised

Make sure the SD card contains only one FAT32 formatted patition. Please check on your computer and format the card if required.

## I am getting an SD not found error

Please check the connections between the shields. Pushing the pins deeper into the sockets sometimes help. Also check the soldering of the pins.


## The wemos is not showing up as a serial device

Please check if you have installed the driver for the USB-Serial adapter (CH340). For Windows and MacOS, you will find the suitable version on the [wemos webpage](https://www.wemos.cc/en/latest/ch340_driver.html). For Linux, usually not driver is required.

## Linux: Cannot connect to the device

The current user has to be in the group *dialout*. Add him by using the following command: `sudo usermod -a -G dialout $USER`