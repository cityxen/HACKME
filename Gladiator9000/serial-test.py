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
serial_timeout = .5
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
    xonxoff=0,
    rtscts=0,
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
        xonxoff=0,
        rtscts=0,
        timeout=serial_timeout
        )

outstring="\n\r"+hostname+"\n\rCityXen Gladiator 9000 Test now active\n\r"
ser1.write(outstring)
if serial_device2!="off":
    ser2.write(outstring)

print("CityXen Gladiator 9000 Test now active")
print("Host: "+hostname)
print("Using configuration:")
print("Serial 1:"+serial_device+" at "+serial_baud+" baud")
if serial_device2!="off":
    print("Serial 2:"+serial_device2+" at "+serial_baud2+" baud")

counter1=0

def dprint(x):
    if debug:
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string+":"+x)


######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # Do Server things

    # Read stuff
    c1=ser1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        # Do things with c1 input
        dprint("S1 RECVd:"+str(len(c1))+":"+c1)

    if serial_device2!="off":
        c2=ser2.readline().lstrip('\x00').rstrip("\x00\n\r")
        if(len(c2)):
            #Do things with c2 input
            dprint("S2 RECVd:"+str(len(c2))+":"+c2)        

    # Write stuff
    x=randrange(1000) # simulate packets
    if x < 200:
        # time.sleep(1)
        counter1+=1
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        ser1.write(b'%s:%d \n\r'%(hostname,counter1))
        if serial_device2!="off":
            ser2.write(b'%s:%d \n\r'%(hostname,counter1))
#            ser2.write(b'%s:Write counter:%d:%s \n\r'%(dt_string,counter1,hostname))


    # Write heartbeat packet
#    counter=counter+1
#    if counter > 1000:
#        now = datetime.now()
#        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#        ser1.write(b'%s:%s g9k test listening\n'%(dt_string,hostname))
#        if serial_device2!="off":
#            ser2.write(b'%s:%s g9k test listening\n'%(dt_string,hostname))
#        counter=0
