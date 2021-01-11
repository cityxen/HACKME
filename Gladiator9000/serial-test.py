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
serial_device  = "/dev/ttyUSB0"
serial_baud    = "1200"
serial_device2 = "off"
serial_baud2   = "1200"
init_test      = False
counter        = 0

print("CityXen Gladiator 9000 Servo Controller Server Test %s - pass -h for help" % (g9ksct_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-s","--serial_device",required=False,help="Serial Device")
ap.add_argument("-b","--serial_baud",required=False,help="Serial Baud Rate")
ap.add_argument("-s2","--serial_device2",required=False,help="Serial Device 2")
ap.add_argument("-b2","--serial_baud2",required=False,help="Serial Baud Rate 2")
args=vars(ap.parse_args())
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
    timeout=None,
    write_timeout=1
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
        timeout=None,
        write_timeout=1
        )    

# Print out a ready message
#ser1.writelines("TEST\n")
#ser1.write(b'CityXen Gladiator 9000 Test now active\n\r')

# ser1.writelines("TEST\n")
# ser1.write(b'CityXen Gladiator 9000 Test now active\n\r')

outstring=hostname+" CityXen Gladiator 9000 Test now active\n"
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

######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # ser1.write(b'Write counter: %d \n'%(counter))
    # counter += 1

    counter1+=1
    ser1.write(b'%s Write counter: %d \n'%(hostname,counter1))
    if serial_device2!="off":
        ser2.write(b'%s Write counter: %d \n'%(hostname,counter1))


    # Do Server things
    c1=ser1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        print("S1 RECVd:"+str(len(c1))+":"+c1)
    if serial_device2!="off":
        c2=ser2.readline().lstrip('\x00').rstrip("\x00\n\r")
        if(len(c2)):
            print("S2 RECVd:"+str(len(c2))+":"+c2)

    counter=counter+1
    if counter > 100:
        ser1.write(b'%s g9k test listening\n'%(hostname))
        if serial_device2!="off":
            ser2.write(b'%s g9k test listening\n'%(hostname))
        counter=0
