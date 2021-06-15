# Upload the logger software to the node

After you have [installed the firmware](firmware.md), you can now upload the application itself. It is located in the [src](../src) directory in this github repository.

To get the software, there are two options

1. Clone this git repository: `git clone https://github.com/ComNets-Bremen/wemos-logger.git`
2. Download this repository as a [zip file](https://github.com/ComNets-Bremen/wemos-logger/archive/refs/heads/master.zip) and unpack it on your local hard disk.

The git version is preferred as new software versions can be pulled directly from the repository (`git pull origin`).

The programming / uploading of the logger software is done in [Visual Studio Code](https://code.visualstudio.com/), an IDE for Windows, Linux and MacOS. The plug-in [pymakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr) is used.

After installing Visual Studio Code and the pymakr plugin including the dependencies, you can open the workspace located in the *src* directory of this repository (File -> Open Workspace). Afterwards, some fine tuning has to be done.

## Setting up Visual Studio Code

### Add wemos nodes to accepted manufacturers

- Press CTRL-ALT-P to open the search dialog
- Enter the word *global*. You will find an entry with the title *Pymakr > Global settings*
- Select this one and press enter.
- A json config file is opened. Check the values for "autoconnect_comport_manufacturers". The following values should be there. Add the missing ones.
    - Pycom
    - Pycom Ltd.
    - FTDI
    - Microsoft
    - Microchip Technology, Inc.
- Save and exit the file

### Make sure autoconnect is disabled in global config

- Press CTRL-ALT-P to open the search dialog
- Enter the word *global*. You will find an entry with the title *Pymakr > Global settings*
- Select this one and press enter.
- A json config file is opened. Change the value for "auto_connect" to False.
- Save and exit the file

### Change the serial port

- Press CTRL-ALT-P to open the search dialog
- Enter the word *settings*. You will find an entry with the title *Pymakr > Project settings*.
- Change the *address* to your serial port id. This depends on your operating system (`COMx`, `/dev/ttyUSBx`, `/dev/ttyACMx`,...)

### Connect to the logger

- Press CTRL-ALT-P to open the search dialog
- Enter the word *connect*. You will find an entry with the title *Pymakr > Connect*.
- In the lower part of the window, you will find a *terminal* tab which now shows the output of the logger. If nothing appears there, press the small reset button on the wemos PCB (small, black button)

### Upload the logger software

- Press CTRL-ALT-P to open the search dialog
- Enter the word *upload*. You will find an entry with the title *Pymakr > Upload project*.
- This will upload the complete project to the logger. The upload status is shown in the terminal tab.


### General problems

Please also check the common issues section for the [Pymakr Plugin](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr)


# TODO / Missing

- TBD
