
#######################################################################################
# Gladiator 9000 Servo Test
#
# 2021 CityXen
#
#
# https://github.com/adafruit/Adafruit_Python_PCA9685
# Credit to Chris Swan https://github.com/cpswan/Python/blob/master/rpi-gpio-jstk.py
#
######################################################################################

from __future__ import division
import time
import Adafruit_PCA9685
import argparse

######################################################################################
# Set up some default variables
g9kst_version  = "1.0"
init_test     = True
counter       = 0
servo_speed   = 4

controller1 = { "x_servo":0,"y_servo":1,"z_servo":2,"x":0,"y":0,"z":0 }
controller2 = { "x_servo":3,"y_servo":4,"z_servo":5,"x":0,"y":0,"z":0 }
controllers = { "1":controller1,"2":controller2 }

print("CityXen Gladiator 9000 Servo Test %s - pass -h for help" % (g9kst_version))

######################################################################################
# Servo initialization stuff
pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
# Configure min and max servo pulse lengths
servo_min = 150 # 150 # Min pulse length out of 4096
servo_max = 600 # 600 # Max pulse length out of 4096
servo_center = ((servo_max//2)+(servo_min//2))
pwm.set_pwm_freq(60)# Set frequency to 60hz, good for servos.

######################################################################################
# Helper functions to make setting a servo pulse width simpler.

def servos_write():
    pwm.set_pwm(controller1["x_servo"],0,controller1["x"])
    pwm.set_pwm(controller1["y_servo"],0,controller1["y"])
    pwm.set_pwm(controller1["z_servo"],0,controller1["z"])
    pwm.set_pwm(controller2["x_servo"],0,controller2["x"])
    pwm.set_pwm(controller2["y_servo"],0,controller2["y"])
    pwm.set_pwm(controller2["z_servo"],0,controller2["z"])

def servos_max():
    controller1["x_servo"]=servo_max
    controller1["y_servo"]=servo_max
    controller1["z_servo"]=servo_max
    controller2["x_servo"]=servo_max
    controller2["y_servo"]=servo_max
    controller2["z_servo"]=servo_max
    servos_write()
    
def servos_center():
    controller1["x_servo"]=servo_center
    controller1["y_servo"]=servo_center
    controller1["z_servo"]=servo_center
    controller2["x_servo"]=servo_center
    controller2["y_servo"]=servo_center
    controller2["z_servo"]=servo_center
    servos_write()

def servos_min():
    controller1["x_servo"]=servo_min
    controller1["y_servo"]=servo_min
    controller1["z_servo"]=servo_min
    controller2["x_servo"]=servo_min
    controller2["y_servo"]=servo_min
    controller2["z_servo"]=servo_min
    servos_write()

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
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-t","--init_test",required=False,help="Test all servos on startup")
ap.add_argument("-s","--servo_speed",required=False,help="Set speed of servo test")
ap.add_argument("-max","--servo_max",action="store_true",required=False,help="Set servos to maximum")
ap.add_argument("-min","--servo_min",action="store_true",required=False,help="Set servos to minimum")
ap.add_argument("-c","--servo_center",action="store_true",required=False,help="Set servos to center")
args=vars(ap.parse_args())
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

x1_dir=servo_speed
y1_dir=servo_speed
z1_dir=servo_speed
x2_dir=servo_speed
y2_dir=servo_speed
z2_dir=servo_speed

servos_center()

while(True):
    # Put stuff here
    # outstr="x:%d y:%d z:%d xdir:%d ydir:%d zdir:%d"%(x,y,z,xdir,ydir,zdir)
    # print(outstr)

    for controller in controllers:
        print(controller)
        controller["x"]+=x1_dir
        if(controller["x"]>servo_max):
            controller["x"]=servo_max
            x1_dir=-(servo_speed//2)
        if(controller["x"]<servo_min):
            controller["x"]=servo_min
            x1_dir=servo_speed
        controller["y"]+=y1_dir
        if(controller["y"]>servo_max):
            controller["y"]=servo_max
            y1_dir=-(servo_speed//2)
        if(controller["y"]<servo_min):
            controller["y"]=servo_min
            y1_dir=servo_speed
        controller["z"]+=z1_dir
        if(controller["z"]>servo_max):
            controller["z"]=servo_max
            z1_dir=-(servo_speed//2)
        if(controller["z"]<servo_min):
            controller["z"]=servo_min
            z1_dir=servo_speed

    servos_write()

