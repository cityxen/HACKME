#######################################################################################
# Gladiator 9000 Servo Controller Server (Test Program)
#
# 2021 CityXen
#
# Takes input from 2 rs-232 serial ports and converts that to servo control
#
# rs-232 Port 1 controls servos (x1,y1,z1)
# rs-232 Port 2 controls servos (x2,y2,z2)
#
# Pinout for serial ports:
# rs-232 Port 1:
#
# rs-232 Port 2:
#
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
serial_device = "/dev/ttyUSB0"
serial_baud   = "9600"
init_test     = False
counter       = 0

print("CityXen Gladiator 9000 Servo Controller Server Test %s - pass -h for help" % (g9ksct_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-s","--serial_device",required=False,help="Serial Device")
ap.add_argument("-b","--serial_baud",required=False,help="Serial Baud Rate")
args=vars(ap.parse_args())
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
    timeout=None
    )

# Print out a ready message
#ser1.writelines("TEST\n")
#ser1.write(b'CityXen Gladiator 9000 Test now active\n\r')

# ser1.writelines("TEST\n")
# ser1.write(b'CityXen Gladiator 9000 Test now active\n\r')

ser1.write(b'CityXen Gladiator 9000 Test now active\n\r')

print("CityXen Gladiator 9000 Test now active")
print("Host: "+hostname)
print("Using configuration:")
print("Serial:"+serial_device+" at "+serial_baud+" baud")

counter1=0

######################################################################################
# Main server program, take input from serial, then send out to servos
while True:

    # ser1.write(b'Write counter: %d \n'%(counter))
    # counter += 1

    counter1 += 1
    if(counter1 >20):
        counter1 = 0
        ser1.write(b'%s Write counter: %d \n'%(hostname),(counter1))

    # Do Server things
    c1=ser1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        print("SER IN STRLEN:"+str(len(c1))+":"+c1)

    counter=counter+1
    if counter > 100:
        ser1.write(b' %s g9k test listening\n'%(hostname))
        print("g9k test listening")
        counter=0
