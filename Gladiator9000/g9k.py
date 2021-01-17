#######################################################################################
# Gladiator 9000
#
# 2021 CityXen
#
# By Deadline & Xamfear
#
#######################################################################################
#
# Required libs and files:
#
# pyserial
# https://github.com/adafruit/Adafruit_Python_PCA9685
#
#######################################################################################

from __future__ import division
import Adafruit_PCA9685
import argparse
from datetime import datetime
from random import randrange
import RPi.GPIO as GPIO
import serial
import socket
import time

######################################################################################
# Set up some default variables
hostname=socket.gethostname()
g9ks_version   = "1.0"
serial_device  = "/dev/ttyUSB0"
serial_baud    = "1200"
serial_device2 = "/dev/ttyAMA0" # "off"
serial_baud2   = "1200"
serial_timeout = .5
init_test      = False
counter        = 0
debug          = False
servos_enabled = True
servo_speed    = 4
servo_freq     = 60
servo_min      = 200 # 150 # Min pulse length out of 4096
servo_max      = 600 # 600 # Max pulse length out of 4096
servo_center   = ((servo_max//2)+(servo_min//2))
x1_dir         = servo_speed
y1_dir         = servo_speed
z1_dir         = servo_speed
x2_dir         = servo_speed
y2_dir         = servo_speed
z2_dir         = servo_speed
controller1    = { "x_servo":0,"y_servo":1,"z_servo":2,"x":0,"y":0,"z":0 }
controller2    = { "x_servo":3,"y_servo":4,"z_servo":5,"x":0,"y":0,"z":0 }
controllers    = { "1":controller1,"2":controller2 }
relay_speed    = .5
joyport_a1     = { "U":37,"UD":False,"D":35,"DD":False,"L":33,"LD":False,"R":31,"RD":False,"F":29,"FD":False } # Assign GPIO (Relay) to Joyport interfaces
joyport_a2     = { "U":23,"UD":False,"D":21,"DD":False,"L":19,"LD":False,"R":15,"RD":False,"F":13,"FD":False }
joyport_b1     = { "U":11,"UD":False,"D":7 ,"DD":False,"L":12,"LD":False,"R":16,"RD":False,"F":18,"FD":False }
joyport_b2     = { "U":22,"UD":False,"D":40,"DD":False,"L":38,"LD":False,"R":36,"RD":False,"F":32,"FD":False }

print("CityXen Gladiator 9000 Server %s - pass -h for help" % (g9ks_version))

######################################################################################
# Some functions
def dprint(x):
    if debug:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string+":"+x)

def servos_write():
    if(servos_enabled):
        pwm.set_pwm(controller1["x_servo"],0,controller1["x"])
        pwm.set_pwm(controller1["y_servo"],0,controller1["y"])
        pwm.set_pwm(controller1["z_servo"],0,controller1["z"])
        pwm.set_pwm(controller2["x_servo"],0,controller2["x"])
        pwm.set_pwm(controller2["y_servo"],0,controller2["y"])
        pwm.set_pwm(controller2["z_servo"],0,controller2["z"])

def servos_max():
    controller1["x"]=servo_max
    controller1["y"]=servo_max
    controller1["z"]=servo_max
    controller2["x"]=servo_max
    controller2["y"]=servo_max
    controller2["z"]=servo_max
    servos_write()
    
def servos_center():
    controller1["x"]=servo_center
    controller1["y"]=servo_center
    controller1["z"]=servo_center
    controller2["x"]=servo_center
    controller2["y"]=servo_center
    controller2["z"]=servo_center
    servos_write()

def servos_min():
    controller1["x"]=servo_min
    controller1["y"]=servo_min
    controller1["z"]=servo_min
    controller2["x"]=servo_min
    controller2["y"]=servo_min
    controller2["z"]=servo_min
    servos_write()

def set_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
    
def set_gpio(): # Relay stuff - Set the GPIO pins from dict values
    GPIO.output(joyport_a1["U"],joyport_a1["UD"])
    GPIO.output(joyport_a1["D"],joyport_a1["DD"])
    GPIO.output(joyport_a1["L"],joyport_a1["LD"])
    GPIO.output(joyport_a1["R"],joyport_a1["RD"])
    GPIO.output(joyport_a1["F"],joyport_a1["FD"])
    GPIO.output(joyport_a2["U"],joyport_a2["UD"])
    GPIO.output(joyport_a2["D"],joyport_a2["DD"])
    GPIO.output(joyport_a2["L"],joyport_a2["LD"])
    GPIO.output(joyport_a2["R"],joyport_a2["RD"])
    GPIO.output(joyport_a2["F"],joyport_a2["FD"])
    GPIO.output(joyport_b1["U"],joyport_b1["UD"])
    GPIO.output(joyport_b1["D"],joyport_b1["DD"])
    GPIO.output(joyport_b1["L"],joyport_b1["LD"])
    GPIO.output(joyport_b1["R"],joyport_b1["RD"])
    GPIO.output(joyport_b1["F"],joyport_b1["FD"])
    GPIO.output(joyport_b2["U"],joyport_b2["UD"])
    GPIO.output(joyport_b2["D"],joyport_b2["DD"])
    GPIO.output(joyport_b2["L"],joyport_b2["LD"])
    GPIO.output(joyport_b2["R"],joyport_b2["RD"])
    GPIO.output(joyport_b2["F"],joyport_b2["FD"])

def all_on(): # Turn all dict values to on
    joyport_a1["UD"]=False
    joyport_a1["DD"]=False
    joyport_a1["LD"]=False
    joyport_a1["RD"]=False
    joyport_a1["FD"]=False
    joyport_a2["UD"]=False
    joyport_a2["DD"]=False
    joyport_a2["LD"]=False
    joyport_a2["RD"]=False
    joyport_a2["FD"]=False
    joyport_b1["UD"]=False
    joyport_b1["DD"]=False
    joyport_b1["LD"]=False
    joyport_b1["RD"]=False
    joyport_b1["FD"]=False
    joyport_b2["UD"]=False
    joyport_b2["DD"]=False
    joyport_b2["LD"]=False
    joyport_b2["RD"]=False
    joyport_b2["FD"]=False

def all_off(): # Turn all dict values to off
    joyport_a1["UD"]=True
    joyport_a1["DD"]=True
    joyport_a1["LD"]=True
    joyport_a1["RD"]=True
    joyport_a1["FD"]=True
    joyport_a2["UD"]=True
    joyport_a2["DD"]=True
    joyport_a2["LD"]=True
    joyport_a2["RD"]=True
    joyport_a2["FD"]=True
    joyport_b1["UD"]=True
    joyport_b1["DD"]=True
    joyport_b1["LD"]=True
    joyport_b1["RD"]=True
    joyport_b1["FD"]=True
    joyport_b2["UD"]=True
    joyport_b2["DD"]=True
    joyport_b2["LD"]=True
    joyport_b2["RD"]=True
    joyport_b2["FD"]=True

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
# Serial stuff
ap.add_argument("-d",    "--debug",required=False,help="Show Debug Output")
ap.add_argument("-comm1", "--serial_device",required=False,help="Serial Device")
ap.add_argument("-comm1b","--serial_baud",required=False,help="Serial Baud Rate")
ap.add_argument("-comm2", "--serial_device2",required=False,help="Serial Device 2")
ap.add_argument("-comm2b","--serial_baud2",required=False,help="Serial Baud Rate 2")
# Servo stuff
ap.add_argument("-ds",   "--disable_servos",required=False,help="Disable servos")
ap.add_argument("-svs",  "--servo_speed",required=False,help="Set speed of servo test")
ap.add_argument("-svmax","--servo_max",action="store_true",required=False,help="Set servos to maximum")
ap.add_argument("-svmin","--servo_min",action="store_true",required=False,help="Set servos to minimum")
ap.add_argument("-svc",  "--servo_center",action="store_true",required=False,help="Set servos to center")
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
if(args["disable_servos"]):
    servos_enabled=False
if(args["servo_speed"]):
    servo_speed=(int(args["servo_speed"]))
if(args["servo_max"]):
    print("Servos set to maximum: %d"%(servo_max))
    servos_max()
    exit(0)
if(args["servo_min"]):
    print("Servos set to minimum: %d"%(servo_min))
    servos_min()
    exit(0)
if(args["servo_center"]):
    print("Servos set to center: %d"%( (servo_max//2)+(servo_min//2) ))
    servos_center()
    exit(0)

print("servos_enabled:%d" % (servos_enabled))

######################################################################################
# Set up serial devices
comm1 = serial.Serial(serial_device,serial_baud,xonxoff=0,rtscts=0,timeout=serial_timeout,
                     bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
if serial_device2!="off":
    comm2 = serial.Serial(serial_device2,serial_baud2,xonxoff=0,rtscts=0,timeout=serial_timeout,
                         bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)

######################################################################################
# Servo initialization stuff - Configure min and max servo pulse lengths
if(servos_enabled):
    pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
    pwm.set_pwm_freq(servo_freq)# Set frequency to 60hz, good for servos.

######################################################################################
# Experimental AI dictionary (igonore)
ai = {
    1: { "hands":controller1, "eyes": {1:joyport_a1, 2:joyport_a2}, "comm":comm1 },
    2: { "hands":controller2, "eyes": {1:joyport_b1, 2:joyport_b2}, "comm":comm2 }
}
print(ai)

######################################################################################
# Send Online Messages
outstring=hostname+" CityXen Gladiator 9000 Online\n"
comm1.write(outstring)
if serial_device2!="off":
    comm2.write(outstring)
print("CityXen Gladiator 9000 Online")
print("Host: "+hostname)
print("Using configuration:")
print("Serial 1:"+serial_device+" at "+serial_baud+" baud")
if serial_device2!="off":
    print("Serial 2:"+serial_device2+" at "+serial_baud2+" baud")

######################################################################################
# Set up GPIO device
GPIO.setwarnings(True) # Ignore some warnings
GPIO.setmode(GPIO.BOARD)
for i in gp2:
    GPIO.setup(i, GPIO.OUT) # Set pins to out
for i in gp3:
    GPIO.setup(i, GPIO.OUT) # Set pins to out
for i in gp4:
    GPIO.setup(i, GPIO.OUT) # Set pins to out

######################################################################################
# Center Servos
servos_center()

######################################################################################
# Main server program, take input from serial, then send out to servos
while True:
    # Do serial stuff
    c1=comm1.readline().lstrip('\x00').rstrip("\x00\n\r")
    if(len(c1)):
        # Do things with c1 input
        dprint("S1 RECVd:"+str(len(c1))+":"+c1)

    if serial_device2!="off":
        c2=comm2.readline().lstrip('\x00').rstrip("\x00\n\r")
        if(len(c2)):
            #Do things with c2 input
            dprint("S2 RECVd:"+str(len(c2))+":"+c2)  

    # Do Servo stuff (Loop servos for now)
    for i in controllers:
        data=controllers[i]
        data["x"]=data["x"]+x1_dir
        if(data["x"]>servo_max):
            data["x"]=servo_max
            x1_dir=-(servo_speed//2)
        if(data["x"]<servo_min):
            data["x"]=servo_min
            x1_dir=servo_speed
        data["y"]=data["y"]+y1_dir
        if(data["y"]>servo_max):
            data["y"]=servo_max
            y1_dir=-(servo_speed//2)
        if(data["y"]<servo_min):
            data["y"]=servo_min
            y1_dir=servo_speed
        data["z"]=data["z"]+z1_dir
        if(data["z"]>servo_max):
            data["z"]=servo_max
            z1_dir=-(servo_speed//2)
        if(data["z"]<servo_min):
            data["z"]=servo_min
            z1_dir=servo_speed
        dprint(data)
    servos_write()            

    # Read Camera Motion Tracking
    # Convert to 8 bit resolution (0-255)
    # 2 MSB will be used for axis, ie: X, Y, Z
    # 01 = X
    # 10 = Y
    # 11 = Z

    # Do Relay Stuff

    '''
    for i in gp2:
        dprint(i)
        gp2[i]=False
        set_gpio()
        time.sleep(speed)
        gp2[i]=True
        set_gpio()
    for i in gp3:
        dprint(i)
        gp3[i]=False
        set_gpio()
        time.sleep(speed)
        gp3[i]=True
        set_gpio()
    for i in gp4:
        dprint(i)
        gp4[i]=False
        set_gpio()
        time.sleep(speed)
        gp4[i]=True
        set_gpio()
    '''

