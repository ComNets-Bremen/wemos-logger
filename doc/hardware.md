# How to assemble the hardware

This project is based on cheap and easy to assemble hardware, namely the wemos nodes. The modules are available online: [wemos.cc](https://www.wemos.cc).

## The modules

We are using four modules which can be stacked together (left to right):

![The brand new parts](img/modules_raw.jpg "The brand new parts") 

1. The D1 which is basically the esp8266 board (very left). Different versions are available. The depicted one is the *D1 mini*. [Overview of D1 modules](https://www.wemos.cc/en/latest/d1/index.html)

2. The Sensor shield. Here, we are using the DHT shield which is equipped with an AM2320 sensor. [DHT Shield](https://www.wemos.cc/en/latest/d1/index.html)

3. A micro SD card shield. [MicroSD card shield](https://www.wemos.cc/en/latest/d1_mini_shield/micro_sd.html)

4. A button shield. [Button shield](https://www.wemos.cc/en/latest/d1_mini_shield/1_button.html)

5. For the SD card shield, an SD card is required.

The nodes are soldered completely. Only the pins have to be soldered as the type of pins depend on the application scenario. Three types of pins are available:

![ ](/home/jd/src/comnets-github/wemos-logger/doc/img/pins.jpg  "Three types of pins")

1. The pins on the very left side of the picture are connected through the PCB, i.e. the PCBs can be stacked. Here, different types and qualities are available.

2. The *normal* pins (as the ones in the center) can only connect to the lower part. This type is used only for the button -- it does not make sense to stack something above the button!

3. The right shows the socket. This can be used for the most bottom shield as in our case the sensor shield. We decided to use the connect through pins to simplify further adaptations.

## How to assemble the hardware

In general, three important things have to be considered when assembling the hardware:

- **Correct alignment**: Make sure that the PCBs are not rotated, i.e., TX, RST, 3V3 and 5V are always on the same corners of the PCB even after stacking!
- **Correct angle of the pins** (90 degrees to the PCB). To properly stack the PCBs, the pins have to be aligned properly. Otherwise, the contact might not work as expected and the PCBs might break.
- **Good soldering** -- especially for the SD card. Otherwise, connection errors can occur.

