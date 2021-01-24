#!/usr/bin/env python
#######################################################################################
# Gladiator 9000 Serial Test Program
#
# 2021 CityXen
#
######################################################################################

from __future__ import division
import time
import serial
import argparse
import socket
from datetime import datetime
from random import randrange

######################################################################################
# Set up some default variables
hostname=socket.gethostname()
g9kst_version  = "1.0"
serial_device  = "/dev/ttyUSB0"
serial_baud    = "1200"
serial_device2 = "off"
serial_baud2   = "1200"
serial_timeout = .6
serial_xonxoff = False
serial_rtscts  = False
init_test      = False
counter        = 0
debug          = False

print("CityXen Gladiator 9000 Serial Test %s - pass -h for help" % (g9kst_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-d","--debug",required=False,help="Show Debug Output")
ap.add_argument("-s","--serial_device",required=False,help="Serial Device")
ap.add_argument("-b","--serial_baud",required=False,help="Serial Baud Rate")
ap.add_argument("-s2","--serial_device2",required=False,help="Serial Device 2")
ap.add_argument("-b2","--serial_baud2",required=False,help="Serial Baud Rate 2")
args=vars(ap.parse_args())
if(args["debug"]):
    debug=True
if(args["serial_device"]):
    serial_device=args["serial_device"]
if(args["serial_baud"]):
    serial_baud = args["serial_baud"]
args=vars(ap.parse_args())
if(args["serial_device2"]):
    serial_device2=args["serial_device2"]
if(args["serial_baud2"]):
    serial_baud2 = args["serial_baud2"]
######################################################################################
# Set up serial device 1
ser1 = serial.Serial(
    serial_device,
    serial_baud,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    xonxoff=serial_xonxoff,
    rtscts=serial_rtscts,
    timeout=serial_timeout
    )

######################################################################################
# Set up serial device 2
if serial_device2!="off":
    ser2 = serial.Serial(
        serial_device2,
        serial_baud2,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        xonxoff=serial_xonxoff,
        rtscts=serial_rtscts,
        timeout=serial_timeout
        )

# print("cityXen gladiator 9000 online")
print("Host: "+hostname)
print("Using configuration:")
print("Serial 1:"+serial_device+" at "+serial_baud+" baud")
if serial_device2!="off":
    print("Serial 2:"+serial_device2+" at "+serial_baud2+" baud")

counter1=0

def dprint(x):
    if debug:
        print("Debug:"+x.lstrip('\x00\n\r').rstrip("\x00\n\r"))
        #print(ord(x[0]))
        #print(ord(x[-1]))

outstring="\n\r\x9ecITYxEN \x9cgladiator \x9e9000 \x1eonline\n\r"
ser1.write(outstring)
if serial_device2!="off":
    ser2.write(outstring)

######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # Do Server things

    # Read stuff
    c1=ser1.readline().lstrip('\x00\n\r').rstrip("\x00\n\r")
    if(len(c1)):
        # Do things with c1 input
        dprint("COMM1 Rx:"+str(len(c1))+":"+c1)

    if serial_device2!="off":
        c2=ser2.readline().lstrip('\x00\n\r').rstrip("\x00\n\r")
        if(len(c2)):
            #Do things with c2 input
            dprint("COMM2 Rx:"+str(len(c2))+":"+c2)

    # Write stuff
    x=randrange(1000) # simulate packets
    if x < 300:
        counter1+=1
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	dprint(b'COMM# Tx:%s:%d\n\r'%(hostname,counter1))
        ser1.write(b'%s:%d\n\r'%(hostname,counter1))
        if serial_device2!="off":
            ser2.write(b'%s:%d\n\r'%(hostname,counter1))

    x=randrange(1000) # send a ident request
    if x < 200:
	dprint("COMM# Tx:IDENTIFY")
        string="identify"
        ser1.write(b'%s\n\r'%(string))
        if serial_device2!="off":
            ser2.write(b'%s\n\r'%(string))

