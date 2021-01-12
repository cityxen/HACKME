
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

print("CityXen Gladiator 9000 Servo Test %s - pass -h for help" % (g9kst_version))

######################################################################################
# Servo initialization stuff
pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
# Configure min and max servo pulse lengths
servo_min = 150 # 150 # Min pulse length out of 4096
servo_max = 600 # 600 # Max pulse length out of 4096
pwm.set_pwm_freq(60)# Set frequency to 60hz, good for servos.

######################################################################################
# Helper functions to make setting a servo pulse width simpler.

def servos_max():
    pwm.set_pwm(0,0,servo_max)
    pwm.set_pwm(1,0,servo_max)
    pwm.set_pwm(2,0,servo_max)
    pwm.set_pwm(3,0,servo_max)
    pwm.set_pwm(4,0,servo_max)
    pwm.set_pwm(5,0,servo_max)
    pwm.set_pwm(6,0,servo_max)

def servos_center():
    pwm.set_pwm(0,0,((servo_max//2)+(servo_min//2)))
    pwm.set_pwm(1,0,((servo_max//2)+(servo_min//2)))
    pwm.set_pwm(2,0,((servo_max//2)+(servo_min//2)))
    pwm.set_pwm(3,0,((servo_max//2)+(servo_min//2)))
    pwm.set_pwm(4,0,((servo_max//2)+(servo_min//2)))
    pwm.set_pwm(5,0,((servo_max//2)+(servo_min//2)))
    pwm.set_pwm(6,0,((servo_max//2)+(servo_min//2)))

def servos_min():
    pwm.set_pwm(0,0,servo_min)
    pwm.set_pwm(1,0,servo_min)
    pwm.set_pwm(2,0,servo_min)
    pwm.set_pwm(3,0,servo_min)
    pwm.set_pwm(4,0,servo_min)
    pwm.set_pwm(5,0,servo_min)
    pwm.set_pwm(6,0,servo_min)


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

xdir=servo_speed
ydir=servo_speed
zdir=servo_speed

x=servo_max//2
y=servo_max//2
z=servo_max//2

pwm.set_pwm(0,0,x)
pwm.set_pwm(1,0,y)
pwm.set_pwm(2,0,z)
pwm.set_pwm(3,0,x)
pwm.set_pwm(4,0,y)
pwm.set_pwm(5,0,z)
pwm.set_pwm(6,0,x)

while(True):
    #global xdir
    #global ydir
    #global zdir
    #global servo_speed

    # Put stuff here
    outstr="x:%d y:%d z:%d xdir:%d ydir:%d zdir:%d"%(x,y,z,xdir,ydir,zdir)
    print(outstr)

    x=x+xdir
    if(x>servo_max):
        x=servo_max
        xdir=-(servo_speed//2)
    if(x<servo_min):
        x=servo_min
        xdir=servo_speed

    y=y+zdir
    if(y>servo_max):
        y=servo_max
        ydir=-(servo_speed//2)
    if(y<servo_min):
        y=servo_min
        ydir=servo_speed

    z=z+zdir
    if(z>servo_max):
        z=servo_max
        zdir=-(servo_speed//2)
    if(z<servo_min):
        z=servo_min
        zdir=servo_speed

    pwm.set_pwm(0,0,x)
    pwm.set_pwm(1,0,y)
    pwm.set_pwm(2,0,z)
    pwm.set_pwm(3,0,x)
    pwm.set_pwm(4,0,y)
    pwm.set_pwm(5,0,z)
    pwm.set_pwm(6,0,x)

