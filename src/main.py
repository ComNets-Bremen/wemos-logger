"""
Simple logger based on esp8266 with wemos shields (-> wemos.cc)

Wiring:
- DHT22 connected to pin 2 (D4, default)
- Button shield connected to pin 0 (D3, default)
- SD-shield connected to SPI with CS on pin 15 (D8) -- depends on board!

Important things:
- After start: read every INTERVAL seconds data and store them to SD card with filename DATA_<number>
- The number is increased after each restart of if the max file size is exceeded (default 1M)
- Press the button for 15..20 secs -> format sd card
- Press the button for 5..10 secs -> start AP with webserver on IP 192.168.4.1
- Press the button for less than 5 secs -> return to normal operation. (currently not working)
- The webserver is blocking, i.e. a restart is required to continue normal operation!
- Webserver SSID MicroPython-<id>, default password: UHB2021Summer
- URLs: http://192.168.4.1/ -> List all sensor data on sd card as json array with the data path
    http://192.168.4.1/DATA_1 -> Get sensor readings from this file as a json file
- Numbering of files starts with 1 (i.e. DATA_1)
- If file does not exist -> default to index

Jens Dede <jd@comnets.uni-bremen.de>
2021
"""

import os
import dht
import machine
import network
import sdcard
import utime as time
import ujson as json
import esp
from webserver import SimpleWebserver


# Pin definitions
DHT_PIN = 2 #D4
BUTTON_PIN = 0 #D3
SD_CS = 15 #D8

# SPI on GPIO 12, 13, 14 / D6, D7, D5

DATA_FILENAME = "DATA_"
DATA_MAX_FILE_SIZE = 1*1000*1000 # 1M
INTERVAL = 60 # secs
AP_PASSWORD = "UHB2021Summer"

SENSOR_RETRY = 3
SENSOR_RETRY_DELAY = 0.2

SOCKET_TIMEOUT = 10

# state definitions
STATE_FORMAT_SD = 1
STATE_START_WEBSERVER = 2
STATE_NORMAL = 3

state = STATE_NORMAL # default state

last_button_state_change = None

# Store data to the given filename, return if a new file should be created (> 1M)
def store_data(filename, data):
    with open(filename, "a") as outfile:
        print("Writing", filename)
        outfile.write(json.dumps(data) + "\n")
        print("Filesize of", filename,":", outfile.tell())
        return outfile.tell() < DATA_MAX_FILE_SIZE

# Create an empty data storeage file
def create_empty_file(filename):
    print("Creating empty file", filename)
    open(filename, 'a').close()

# Read the sensor values and return them as a dict
def read_sensors():
    retry = 0
    while retry < SENSOR_RETRY:
        try:
            res = {}
            dht_sensor.measure()
            time.sleep(1)
            res["humidity"] = dht_sensor.humidity()
            res["temperature"] = dht_sensor.temperature()
            res["retry"] = retry

            res["time"] = time.time()
            return res
        except:
            retry += 1
            time.delay(SENSOR_RETRY_DELAY)
        print("Cannot read sensor")
        return None

# Read the stored data from the sd card and remove the files if requested
def read_stored_data(path="/sd/", remove = False):
    for f in os.listdir(path):
        if f.startswith(DATA_FILENAME):
            print("FILE ", f)
            with open(path+f, "r") as infile:
                for line in infile:
                    print(line, end="")
                print("")
            if remove:
                os.remove(path+f)

# Handle (and decrypt) the button actions
def button_handler(pin):
    global last_button_state_change
    global state
    if not last_button_state_change == None:
        duration = time.time() - last_button_state_change
        if 1 < duration < 5 and pin.value():
            state = STATE_NORMAL
        elif 5 <= duration <= 10 and pin.value():
            state = STATE_START_WEBSERVER
        elif 15 <= duration <= 20 and pin.value():
            state = STATE_FORMAT_SD
        else:
            pass

    last_button_state_change = time.time()

# Perform the measurement and store the results to the sd card
def do_measure():
    global new_fileid
    global filename
    data = {}
    data["id"] = esp.flash_id()
    data["data"] = read_sensors()
    print(data)

    if not store_data(filename, data):
        # Exceeded file limit, create new file
        new_fileid = new_fileid + 1
        filename = "/sd/" + DATA_FILENAME + str(new_fileid)
        create_empty_file(filename)



# Disable all network functionality per default
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

sws = SimpleWebserver()

dht_sensor = dht.DHT22(machine.Pin(DHT_PIN))

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING, handler=button_handler)


# Get SD card
try:
    sd = sdcard.SDCard(machine.SPI(1), machine.Pin(SD_CS))
except OSError:
    print("No sd card")
    sd = None

if sd:
    try:
        os.mount(sd, '/sd')
        print(os.listdir('/sd/'))
    except:
        print("Cannot mount sd card")

# TODO: What should be done if no SD card is present?

# Get highest file id number from sd card
new_fileid = 0
for fn in os.listdir('/sd'):
    try:
        new_fileid = max(new_fileid, int(fn.split("_")[1]))
    except:
        # file named in different format
        pass

new_fileid += 1
filename = "/sd/" + DATA_FILENAME + str(new_fileid)
print("Storing new data to", new_fileid, filename)

time.sleep(2) # Wait 2 secs to ensure everything is initiated properly (especially the DHT sensor)

next_measure_interval = time.time()

# Main loop
while True:

    if next_measure_interval <= time.time() or next_measure_interval > time.time() + (2*INTERVAL):
        # It's time to perform some measurements...
        next_measure_interval = time.time() + INTERVAL
        do_measure()

    if state == STATE_FORMAT_SD and not sws.is_running():
        if sd:
            print("Start formatting sd card")
            os.umount('/sd')
            os.VfsFat.mkfs(sd)
            os.mount(sd, '/sd')
            new_fileid = 1
            filename = "/sd/" + DATA_FILENAME + str(new_fileid)

            print("Done")
        else:
            print("SD access error")

        state = STATE_NORMAL

    elif state == STATE_START_WEBSERVER:
        if not sws.is_running():
            ap_if = network.WLAN(network.AP_IF)
            ap_if.active(True)
            ap_if.config(password = AP_PASSWORD)
            while(not ap_if.active()):
                pass

            sws.serve(SOCKET_TIMEOUT)

            print("Server started @", ap_if.ifconfig())

    elif state == STATE_NORMAL and sws.is_running():
        sws.stop_serve()
        network.WLAN(network.AP_IF).active(False)
        print("Server disabled")
        

    # Needs to be called regularly if the webserver is running
    if sws.is_running():
        sws.cyclic_handler()
    