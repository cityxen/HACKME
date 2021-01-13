#######################################################################################
# 232-ATSC Controller
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
g9ksct_version = "1.0"
serial_device  = "/dev/ttyAMA0"
serial_baud    = "9600"
init_test      = False
counter        = 0
debug          = False

print("CityXen 232-ATSC Controller %s - pass -h for help" % (g9ksct_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-d","--debug",required=False,help="Show Debug Output")
ap.add_argument("-s","--serial_device",required=False,help="Serial Device")
ap.add_argument("-b","--serial_baud",required=False,help="Serial Baud Rate")
args=vars(ap.parse_args())
if(args["debug"]):
    debug=True
if(args["serial_device"]):
    serial_device=args["serial_device"]
if(args["serial_baud"]):
    serial_baud = args["serial_baud"]
######################################################################################
# Set up serial device 1
ser1 = serial.Serial(
    serial_device,
    serial_baud,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    xonxoff=0,
    rtscts=0,
    timeout=1
    )

def dprint(x):
    if debug:
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string+":"+x)


######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # Read stuff
    c1=ser1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        # Do things with c1 input
        dprint("S1 RECVd:"+str(len(c1))+":"+c1)

    # Check key input

    # Write stuff
    #    ser1.write(b'%s:Write counter:%d:%s \n'%(dt_string,counter1,hostname))