#######################################################################################
# Gladiator 9000 Servo Controller Server
#
# 2021 CityXen
#
# Takes input from 2 rs-232 serial ports and converts that to servo control
#
# rs-232 Port 1 controls servos (x1,y1,z1)
# rs-232 Port 2 controls servos (x2,y2,z2)
#
# https://github.com/adafruit/Adafruit_Python_PCA9685
# Credit to Chris Swan https://github.com/cpswan/Python/blob/master/rpi-gpio-jstk.py
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
import Adafruit_PCA9685
import serial
import argparse

######################################################################################
# Set up some default variables
g9ksc_version  = "1.0"
serial_device1 = "/dev/ttyAMA0"
serial_baud1   = "9600"
serial_device2 = "/dev/ttyUSB0"
serial_baud2   = "9600"
init_test     = False
counter       = 0

print("CityXen Gladiator 9000 Servo Controller Server %s - pass -h for help" % (g9ksc_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-s1","--serial_device1",required=False,help="Serial 1 Device")
ap.add_argument("-b1","--serial_baud1",required=False,help="Serial 1 Baud Rate")
ap.add_argument("-s2","--serial_device2",required=False,help="Serial 2 Device")
ap.add_argument("-b2","--serial_baud2",required=False,help="Serial 2 Baud Rate")
ap.add_argument("-t","--init_test",required=False,help="Test all relays on startup")
args=vars(ap.parse_args())
if(args["serial_device1"]):
    serial_device1=args["serial_device1"]
if(args["serial_baud1"]):
    serial_baud1 = args["serial_baud1"]
if(args["serial_device2"]):
    serial_device2=args["serial_device2"]
if(args["serial_baud2"]):
    serial_baud2 = args["serial_baud2"]
if(args["init_test"]):
    init_test   = True if (args["init_test"]=="1") else False

######################################################################################
# Set up serial device 1
ser1 = serial.Serial(serial_device1,serial_baud1,
    parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,xonxoff=0,timeout=None,rtscts=0 )
######################################################################################
# Set up serial device 2
"""
ser2 = serial.Serial(serial_device2,serial_baud2,
    parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,xonxoff=0,timeout=None,rtscts=0)
"""

######################################################################################
# Servo initialization stuff
pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
# Configure min and max servo pulse lengths
servo_min = 150 # 150 # Min pulse length out of 4096
servo_max = 600 # 600 # Max pulse length out of 4096
pwm.set_pwm_freq(60)# Set frequency to 60hz, good for servos.

######################################################################################
# Helper functions to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


######################################################################################
# Some final preparation before server starts

pwm.set_pwm(0,0,servo_min)
pwm.set_pwm(1,0,servo_min)
pwm.set_pwm(2,0,servo_min)

controller1 = {
    0:0,
    1:1,
    2:2,
    "x":servo_min,
    "y":servo_min,
    "z":servo_min
}
controller2 = {
    0:3,
    1:4,
    2:5,
    "x":servo_min,
    "y":servo_min,
    "z":servo_min
}

controller1["x"]=servo_max//2;
controller1["y"]=servo_max//2;
controller1["z"]=servo_max//2

controller2["x"]=servo_max//2;
controller2["y"]=servo_max//2;
controller2["z"]=servo_max//2;

pwm.set_pwm(0,0,controller1["x"])
pwm.set_pwm(1,0,controller1["y"])
pwm.set_pwm(2,0,controller1["z"])

# Print out a ready message
ser1.println('CityXen Gladiator 9000 now active')
# ser2.write(b'CityXen Gladiator 9000 now active\n\r')
print("CityXen Gladiator 9000 now active")
print("Using configuration:")
print("Serial 1:"+serial_device1+" at "+serial_baud1+" baud")
# print("Serial 2:"+serial_device2+" at "+serial_baud2+" baud")

######################################################################################
# TODO: Set up test sequence for this
# Do or do not, there is no try...
#if(init_test):
#    print("Initialization Test")
#    test_sequence() # Do a quick system test

######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # Do Server things
    c1=ser1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        print("SER1 IN STRLEN:"+str(len(c1))+":"+c1)
    #c2=ser2.readline().lstrip('\x00').rstrip("\x00\n\r")
    #if(len(c2)):
    #    print("IN STRLEN:"+str(len(c2))+":"+c2)

    if(c1[0]=="f"):
        print('C1 FIRE!')
        controller1["z"]+=20
        if(controller1["z"]>servo_max):
            controller1["z"]=servo_min

    pwm.set_pwm(controller1[2],0,controller1[z])
    # pwm.set_pwm(1,0,y)
    # pwm.set_pwm(2,0,z)        

    counter=counter+1
    if counter > 1000:
        ser1.write(b'g9k listening\n\r')
        print("g9k listening")
        counter=0

"""
    if(right):
        x=x+5
        if(x>4vo_max):
            x=servo_max
        print('x=%d'%x)
    if(left):
        x=x-5
        if(x<servo_min):
            x=servo_min
        print('x=%d'%x)
    if(up):
        y=y+5
        if(y>servo_max):
            y=servo_max
        print('y=%d'%y)
    if(down):
        y=y-5
        if(y<servo_min):
            y=servo_min
        print('y=%d'%y)
"""


