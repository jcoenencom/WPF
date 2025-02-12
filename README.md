Connection of a Stiebel Eltron heat pump (WPF16) onto a knx Bus.

![IMG_9426](https://github.com/jcoenencom/WPF/assets/11938043/2b6d179b-0c5c-475b-a32c-5add19b8f46f)

This project uses a raspberry pi CAN bus interface (MCP2515 Can controller + MCP2551 Transceiver on the RPi's SPI interface) on the CAn' side and connects to the KNX bus via ethernet (either to a KNX/IP router or an instance of knxd).

Several CAN bus interfaces have been successfully tested, the skpang.co.uk PICAN rev B (replaced by the PICAN 2), coming from from an older version of the project installed on a raspberry pi model B; the sensing of the WPF was done by a stiebel modem with software from stiebel running on a windows XP virtual machine, the raspberry was monitoring the responses from the WPF controller. A cumbersome configuration.
Other CAN bus interfaces tested: Waveshare RS485-CAN HAT and USB2CAN converter.

After many years the SD card of the rasspberry failed, as I lost the original code, I decided to rewrite it.

Here are the raspberry configuration steps:

Installed lastest Raspbian 12.1 Bookworm.

Make sure it's up to date ...

sudo apt-get update
suddo apt-get upgrade

reboot

Add the overlays in /boot/config.txt

dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=spi-bcm2835-overlay 

reboot

after that the interface can be brought up at 20 KHz (WPF bus speed):

sudo /sbin/ip link set can0 up type can bitrate 20000

Doing an ifconfig should indicate the interface


$ ifconfig can0
can0: flags=193<UP,RUNNING,NOARP>  mtu 16
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 65536  (UNSPEC)
        RX packets 1059560  bytes 7416724 (7.0 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 178702  bytes 893510 (872.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


Some tools are available from http://www.skpang.co.uk/dl/can-test_pi2.zip

These tools are usefull to play with the interface (eg. candump to dump the message recieved on the bus)

$ candump can0
  can0  683   [7]  61 0F 01 00 DC 00 00
  can0  683   [7]  C1 01 01 00 DC 00 00
  can0  601   [7]  D2 03 01 00 00 00 00
  can0  683   [7]  C1 01 FA 01 0D 00 DC
  can0  601   [7]  D2 03 FA 01 0D 03 E8
  can0  683   [7]  C1 02 01 00 DC 00 00
  can0  602   [7]  D2 03 01 00 00 00 00
  can0  683   [7]  C1 02 FA 01 0D 00 DC
  can0  602   [7]  D2 03 FA 01 0D 00 05
  can0  683   [7]  C1 03 01 00 DC 00 00
  can0  700   [5]  C1 01 FA 00 0F
  can0  601   [7]  E2 00 FA 00 0F 00 CB
  can0  683   [7]  C1 04 01 00 DC 00 00

INSTALLATION OF PYTHON LIBRARIES

Can bus libraries:

First allow for system wide package installation with pip (there's a python-can library in debian package, but probably not the latest)

sudo nano /etc/pip.conf 

add the following line
break-system-packages = true

then proceed with package installation

sudo pip install python-can

That's it for the preparation of the system.

Get the code from github.

File are:

WPF.ini holds the configuration file in sections:

    [CANBUS]                    #the CAN bus definition
    bustype="socket"            #type
    channel="can0"              #which channel to use in case multiple bus defined
    timer=5                     #timer (seconds) between CAN bus requests
    
    [KNX] the KNX gateway defintion
    gateway=192.168.1.18

    [readings] what are the WPF reading that should be monitored
    file=elster.json

    [debug] usual debug on/off
    level=i


in this case, the file elster.json holds the definition of the monitored parameters

For example:

{ "0xe":{             # the command sent on the bus to request the data
    "nom":"TECS",     # description the data, Temperature of the warm water circuit
    "grpaddr":"4/2/3",# KNX group address allocated to the parameter
    "dpt":"9",        # KNX data point type (dpt.9 is temperature)
    "candest": 1,     # CAN controller destination
    "unit":0          # CAN unit destination, these 2 are used to send the correct frame on the CAN bus
}

knx.py is a simple knx python library (pypi.org knx 0.4.0), with an added dpt9.0conversion function

myknx.py some encoding function (not really is use anymore as the dpt9 has been moved to knx.py)

wpfknx.py class package of the monitored objects.

wpf-knx.py main program.


The program will read the config file and object defintions, connect the buses (CAN/KNX), define the objects and will loop through the objects, sending a request every CAN timer seconds between objects. The WPF replies will be CAN decoded, KNX encoded and sent on the KNX bus as they come in.

The system has been running now for 10 days without a glitch or drops.

A former version using xknx python library (as in Homeassistant) did not perofmred as well (after a few hours KNX connection would drop out or the program would crash), so it was not retained.

To test the setup, run the program

$chmod a+x wpf-kns.py #make sure the program can run

and launch it


$ ./wpf-knx.py 
Starting can bus reading of WPF info, writing to KNX bus
[CANBUS]
	for key bustype -> "socket" (value)
	for key channel -> "can0" (value)
	for key timer -> 5 (value)
[KNX]
	for key gateway -> 192.168.1.18 (value)
[readings]
	for key file -> /etc/WPF/elster.json (value)
[debug]
	for key level -> 'i' (value)
[nothing]
/etc/WPF/elster.json
debug info
KNX bus successfully connected on 
{'nom': 'TECS', 'grpaddr': '4/2/3', 'dpt': '9', 'candest': 1, 'unit': 0}
{'nom': 'T ambiante', 'grpaddr': '4/2/1', 'dpt': '9', 'candest': 2, 'unit': 1}
{'nom': 'T Retour', 'grpaddr': '4/2/5', 'dpt': '9', 'candest': 1, 'unit': 0}
{'nom': 'T Départ', 'grpaddr': '4/2/4', 'dpt': '9', 'candest': 1, 'unit': 0}
{'nom': 'T Extérieure', 'grpaddr': '4/2/0', 'dpt': '9', 'candest': 1, 'unit': 0}
{'nom': 'T Source', 'grpaddr': '4/2/2', 'dpt': '9', 'candest': 1, 'unit': 0}
{'nom': 'T Mélangeur', 'grpaddr': '4/2/6', 'dpt': '9', 'candest': 4, 'unit': 1}
Curently defined object in  /etc/WPF/elster.json
TECS 	 4/2/3 	 9 	 0  current value: 0

T ambiante 	 4/2/1 	 9 	 1  current value: 0

T Retour 	 4/2/5 	 9 	 0  current value: 0

T Départ 	 4/2/4 	 9 	 0  current value: 0

T Extérieure 	 4/2/0 	 9 	 0  current value: 0

T Source 	 4/2/2 	 9 	 0  current value: 0

T Mélangeur 	 4/2/6 	 9 	 1  current value: 0

TECS comd  [49, 0, 250, 0, 14]
T ambiante comd  [97, 1, 250, 0, 17]
T Retour comd  [49, 0, 250, 0, 22]
T Départ comd  [49, 0, 250, 1, 214]
T Extérieure comd  [49, 0, 250, 0, 12]
T Source comd  [49, 0, 250, 1, 212]
T Mélangeur comd  [193, 1, 250, 0, 15]
sending a request to the can bus (wpf) every  5  seconds
sending request for  TECS 	 [49, 0, 250, 0, 14] set  TECS  in knx group  4/2/3 to  49.0
sending request for  T ambiante 	 [97, 1, 250, 0, 17] set  T Source  in knx group  4/2/2 to  22.0
set  T ambiante  in knx group  4/2/1 to  22.4
set  T Mélangeur  in knx group  4/2/6 to  20.3
sending request for  T Retour 	 [49, 0, 250, 0, 22] set  T Retour  in knx group  4/2/5 to  22.6
set  TECS  in knx group  4/2/3 to  49.0
sending request for  T Départ 	 [49, 0, 250, 1, 214] set  T Départ  in knx group  4/2/4 to  25.9
set  T ambiante  in knx group  4/2/1 to  22.4
sending request for  T Extérieure 	 [49, 0, 250, 0, 12] set  T Extérieure  in knx group  4/2/0 to  19.9
set  T Retour  in knx group  4/2/5 to  22.6
sending request for  T Source 	 [49, 0, 250, 1, 212] set  T Source  in knx group  4/2/2 to  22.0
set  T Départ  in knx group  4/2/4 to  25.9
sending request for  T Mélangeur 	 [193, 1, 250, 0, 15] set  T Mélangeur  in knx group  4/2/6 to  20.3










System implementation:

	sudo mkdir /etc/WPF
	sudo cp WPF.ini /etc/WPF/
	sudo cp elster.json /etc/WPF/
	sudo cp knx.py /usr/local/lib/python3.11/dist-packages/
	sudo cp myknx.py /usr/local/lib/python3.11/dist-packages/
	sudo cp wpfknx.py /usr/local/lib/python3.11/dist-packages/
	sudo cp wpf-knx.py /usr/local/bin


Installed a systemctl service to start the program when rebooting and restart it if crashing:

	sudo nano /etc/systemd/system/wpfknx.service 
insert 

	[Unit]
	Description=WPF CAN to KNX translator
	After=syslog.target network-online.target

	[Service]
	Type=simple
	User=jcoenen
	ExecStart=/usr/local/bin/wpf-knx.py > /var/log/wpfknx.log 2>&1
	Restart=on-failure
	RestartSec=10
	KillMode=process

	[Install]
	WantedBy=multi-user.target


Then:

	sudo systemctl start wpfknx
	sudo systemctl enable wpfknx

Make sure the CAN bus comes up after reboot:

	sudo nano /etc/modules-load.d/can.conf
insert:

	can
	can_raw

Then define the new interfce in the network configuration (networkd)

	sudo nano /etc/systemd/network/80-can.network

	[Match]
	Name=can0
	[CAN]
	BitRate=20K
	RestartSec=100ms

 Bookworm uses network manager, it is therefore necessary to enable and run networkd (can run concurently)

	sudo systemctl start systemd-networkd
	sudo systemctl enable systemd-networkd


