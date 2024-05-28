#!/usr/bin/python

import os
import can
import time
import struct
import json
import configparser
import myknx
from wpfknx import wpf
import asyncio
from knx import connect

debug = False

def can_parser(msg):
### can_parser(msg)
###    msg: can.message
### gets called when a new message is received at the can bus instance
### interpret the contents and set the read value in the object
###
  global wpflist
  global debug
  

#  msg hold the can frame received
# message from PAC
# and check == bcheck :
  #print(msg, ' data ',msg.data, end ='\t')
  dest = (int.from_bytes(msg.data[0:1])& 0xF0) >> 4 #destination
  msgtype = int.from_bytes(msg.data[0:1])&0xf
  ext = int.from_bytes(msg.data[2:3])
  #print('got can msg ', msg.data , ' to ', hex(dest), ' of type ', hex(msgtype), 'ext byte is ',hex(ext))
  if (ext==0xfa):
    bsend = msg.data[3:5]
    sender = int.from_bytes(bsend,'big')
    bval = int.from_bytes(msg.data[5:],'big')/10
  else:
    bsend = msg.data[1:3]
    sender = int.from_bytes(bsend,'big')
    bval = int.from_bytes(msg.data[3:5],'big')/10
#  print(msg.data,'\t',hex(sender))
### if the code is monitored, ie. is in the dict keys
###
  if hex(sender) in wpflist.keys():
    name = wpflist[hex(sender)].nom
    if bval <=1 or bval > 70:
       print('unexpected value: ',bval,' in msg:',msg)
    else:
#
# set the canread value in the object and send it on knx bus
#
       wpflist[hex(sender)].setval(bval)


### print can message

def canprint(msg: can.Message) -> None:
   print(msg, end='')


async def main()-> None:

### define the globals (as main is within the scope of asyncio.run)
### debug: if set will generate debug printouts
### wpfList: Dict of monitored wpf class objects

  global wpflist
  global config
  global xknx
  global debug


  filters = [
      {"can_id": 0x180, "can_mask": 0x7FF, "extended": False},
      {"can_id": 0x301, "can_mask": 0x7FF, "extended": False},
      {"can_id": 0x601, "can_mask": 0x7FF, "extended": False}
  ]


  print('Starting can bus reading of WPF info, writing to KNX bus', flush=True)
  
  #
  # Reading configuration files
  # WPF.ini holds CANBus info, KNXBus info, object definition readings.json and debug section
  #
  
  config = configparser.ConfigParser()
  config.read("/etc/WPF/WPF.ini")

  print('abt to set debug',debug)
  debug = (config['debug']['level'] == 'i')
  print('debug set to',debug, 'coz ',config['debug']['level'])

  if debug: print("Debug Turned on")

  for section in config.sections():
      if debug: print(f"[{section}]", flush=True)
      for key, value in config.items(section):
          if debug: print(f"\tfor key {key} -> {value} (value)", flush=True)

  if debug: print(config['readings']['file'], flush=True)

  if debug: print('debug info', flush=True)


  #
  # read the defined object in a dictionary
  #
  try:
    fname=config['readings']['file']
  except KeyError:
     fname='readings.json'


  fjson=open(fname)
  data = json.load(fjson)

  wpflist={}


  
  try:
     knxgtw = config['KNX']['gateway']
  except KeyError:
     knxgtw = "192.168.1.25"

  xknx = connect(knxgtw)
  can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan', can_filters=filters)# socketcan_native  
  
  print('KNX bus successfully connected on ',)


  for key in data:
    x = data[key]
    if debug: print(x)
    wpflist[key]=wpf(xknx,x['nom'],x['grpaddr'],x['dpt'],x['candest'],x['unit'],can0)


  fjson.close()

  if debug: 
    print ('Curently defined object in ',fname)
  #
  # Iterating through the json to define the wpf readings  objects into an objects dictionry wpflist[]
  # 
    for key in wpflist:
  #    print(wpflist[key], flush=True)
      wpflist[key].print()

  # connecting to the world

  # open the CAN bus

  msg=can0.recv()
  #
  # define the callback routine to process incommig messages
  #
  #loop = asyncio.get_running_loop()

  #notifier = can.Notifier(can0, [can_parser])
  notifier = can.Notifier(can0, [can_parser])

  # load the req dict with the requests from json file

  reqs={}

  TSrce = [0x31,0x00,0xfa,0x01,0xd4]

  for key in data:
      x = data[key]
      rdata= [1 + x['candest']*0x30]
      rdata.extend([x['unit'],250])  #00 FA
      rdata.extend(list((int(key,16)).to_bytes(2,'big')))
      reqs[key]=rdata
      if debug: print(x['nom'], 'comd ', rdata)


### get the timer value from config file default to 60
### the timer seperates two can request messages

  try:
    timer=int(config['CANBUS']['timer'])
  except KeyError:
     timer=60

  print("sending a request to the can bus (wpf) every ",timer,' seconds')

  while True:
    for key in reqs:

      msg = can.Message(arbitration_id=0x700, data=reqs[key], is_extended_id=False)
      try:
         if debug: print('sending request for ', data[key]['nom'],'\t',reqs[key],end=' ')
         can0.send(msg)
      except can.CanError:
            print('message ',msg, ' not sent')
      time.sleep(timer)

  
asyncio.run(main())
