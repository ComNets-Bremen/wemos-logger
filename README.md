# wemos-logger - A basic logger app for esp32 wemos devices

The documentation - especially how to build this logger -  is located in the [doc](doc) directory, the source code for the logger in the [src](src) directory.

# What is this?

For several application scenarios, a simple, easy to assemble, cheap and easy to read out data logger is required. This repository offers such a logger:

* Based on the inexpensive esp8266 microcontroller
* Programmed in Python
* Easy to configure
* Can be read out via a simple web interface
* Flexible and easy extend:
    * Battery
    * Real time clock
    * Other sensors
    * ...

![The logger](doc/img/stack_complete_side.jpg  "The logger")

## Basic functionality

In the basic version, this logger contains a temperature and humidity sensor, the controller board and an SD card for data storage. The sensor is read out every 10 minutes and the data is stored on the SD card.

Additionally, the logger has a button for fundamental user interaction:
* A short press (1 to 5 seconds) changes to the normal operation mode: Collect data every 10 minutes and try to reduce the energy requirements to a minimum-.
* A long press (5 to 10 seconds) starts an access point and a web server. In this mode, the data can be read out from the SD card. After a short press to the button, the device will disable the web server and return to normal operation.
* A very long press (15 to 20 seconds) will format the SD card and remove all measurements.

## The web server

Pressing the button for 5-10 seconds will enable the access point and start the web server:

* **SSID**: `MicroPython-<UNIQUE_ID>`
* **Password**: `UHB2021Summer`
* **Server IP**: `192.168.4.1`

The server will return json documents with the requested data:
* The root document will return a json document listing all available data.
* The data is stored as numbered data URLs using the following format `http://192.168.4.1/DATA_1`. This json document will contain the sensor readings.
* If a non-existent json document is requested, the root index document will be returned.

The following screenshot shows an example of the listing of the available data:

![The index of all available data](doc/img/screenshot_index.png  "The index of all available data")

An excerpt of one data file looks as follows:

![An excerpt of data file](doc/img/screenshot_datasets.png  "An excerpt of data file")

It contains the following data:

* **id**: The id of the node.
* **data**: The measurements from this node. This version contains the following values:
    * **time**: The local timestamp in seconds when the measurement was taken.
    * **humidity**: The measured humidity in percent
    * **temperature**: The measured temperature in degree celcius
    * **retry**: If an error occurred while reading the sensor, this counter is increased. Should be zero in case of no errors.



## General remarks

* In the basic version of this logger, no real time clock (RTC) is used. The timestamps start from 0 after the node was disconnected from the power supply.
* Due to the missing RTC, the timestamps in different DATA files might not be consistent. However, the timestamp in one file should be consistent.

# Known issues

Nothing known... until now.

# License

Jens Dede, Sustainable Communication Networks, University of Bremen, jd@comnets.uni-bremen.de, 2021

This code is licensed under the [GPLv3