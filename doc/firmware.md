Install the pycom firmware

Manual: http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#deploying-the-firmware

Download Firmware: https://micropython.org/download/esp8266/
-> https://micropython.org/resources/firmware/esp8266-20210418-v1.15.bin

esptool

python3 -m venv .

. ./bin/activate
(abc...) vor prompt
pip3 install esptool


esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20210418-v1.15.bin

Done installing upython


