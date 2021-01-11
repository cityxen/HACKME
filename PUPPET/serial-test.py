#######################################################################################
# PUPPET - Pre-scripted Universal Personality Processor Enhancement Tunnel
# Server (Test Program)
#
# 2021 CityXen
#
# Outputs to 1 (or 2) rs-232 serial ports
# 
######################################################################################

from __future__ import division
import time
import serial
import argparse
import socket
hostname=socket.gethostname()

######################################################################################
# Set up some default variables
g9ksct_version = "1.0"
serial_device  = "/dev/ttyUSB0"
serial_baud    = "1200"
serial_encode  = "standard"
serial_device2 = "off"
serial_baud2   = "1200"
serial_encode2 = "standard"
init_test      = False
counter        = 0
debug          = False

print("CityXen PUPPET Server Test %s - pass -h for help" % (g9ksct_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-d","--debug",required=False,help="Show Debug Output")
ap.add_argument("-s","--serial_device",required=False,help="Serial Device")
ap.add_argument("-b","--serial_baud",required=False,help="Serial Baud Rate (300,1200,2400,9600,19200)")
ap.add_argument("-e","--serial_encode",required=False,help="Serial Encoding (standard,clicky,pokey,amy,fido,victoria,tex,trish,apollol)")
ap.add_argument("-s2","--serial_device2",required=False,help="Serial Device 2")
ap.add_argument("-b2","--serial_baud2",required=False,help="Serial Baud Rate 2 (300,1200,2400,9600,19200)")
ap.add_argument("-e2","--serial_encode2",required=False,help="Serial Encoding 2 (standard,clicky,pokey,amy,fido,victoria,tex,trish,apollol)")
args=vars(ap.parse_args())
if(args["debug"]):
    debug=True
if(args["serial_device"]):
    serial_device=args["serial_device"]
if(args["serial_baud"]):
    serial_baud = args["serial_baud"]
if(args["serial_encode"]):
    serial_baud = args["serial_encode"]
args=vars(ap.parse_args())
if(args["serial_device2"]):
    serial_device2=args["serial_device2"]
if(args["serial_baud2"]):
    serial_baud2 = args["serial_baud2"]
if(args["serial_encode2"]):
    serial_baud = args["serial_encode2"]

######################################################################################
# Set up serial device 1
ser1 = serial.Serial(serial_device,serial_baud,xonxoff=0,rtscts=0,timeout=1,
    bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)

######################################################################################
# Set up serial device 2
if serial_device2!="off":
    ser2 = serial.Serial(serial_device2,serial_baud2,xonxoff=0,rtscts=0,timeout=1,
        bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)    

outstring=hostname+" CityXen PUPPET Test now active\n"
ser1.write(outstring)
if serial_device2!="off":
    ser2.write(outstring)

print("CityXen PUPPET Test now active")
print("Host: "+hostname)
print("Using configuration:")
print("Serial 1:"+serial_device+" at "+serial_baud+" baud")
if serial_device2!="off":
    print("Serial 2:"+serial_device2+" at "+serial_baud2+" baud")

counter1=0

def dprint(x):
    if debug:
        print(x)

######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # Do Server things
    counter1+=1

    ser1.write(b'%s Write counter: %d \n'%(hostname,counter1))
    c1=ser1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        # Do things with c1 input
        dprint("S1 RECVd:"+str(len(c1))+":"+c1)

    if serial_device2!="off":
        ser2.write(b'%s Write counter: %d \n'%(hostname,counter1))
        c2=ser2.readline().lstrip('\x00').rstrip("\x00\n\r")
        if(len(c2)):
            #Do things with c2 input
            dprint("S2 RECVd:"+str(len(c2))+":"+c2)

    counter=counter+1
    if counter > 100:
        ser1.write(b'%s g9k test listening\n'%(hostname))
        if serial_device2!="off":
            ser2.write(b'%s g9k test listening\n'%(hostname))
        counter=0
