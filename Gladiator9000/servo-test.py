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
import argparse

######################################################################################
# Set up some default variables
g9kst_version  = "1.0"
init_test     = False
counter       = 0

print("CityXen Gladiator 9000 Servo Test %s - pass -h for help" % (g9kst_version))

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-t","--init_test",required=False,help="Test all servos on startup")
args=vars(ap.parse_args())
if(args["init_test"]):
    init_test   = True if (args["init_test"]=="1") else False

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

#controller1 = {
#    0:0,
#    1:1,
#    2:2,
#   "x":servo_min,
#    "y":servo_min,
#    "z":servo_min
#}
#controller2 = {
#    0:3,
#    1:4,
#    2:5,
#    "x":servo_min,
#    "y":servo_min,
#    "z":servo_min
#}
#controller1["x"]=servo_max//2
#controller1["y"]=servo_max//2
#controller1["z"]=servo_max//2
#controller2["x"]=servo_max//2
#controller2["y"]=servo_max//2
#controller2["z"]=servo_max//2
#pwm.set_pwm(0,0,controller1["x"])
#pwm.set_pwm(1,0,controller1["y"])
#pwm.set_pwm(2,0,controller1["z"])

pwm.set_pwm(0,0,servo_min)
pwm.set_pwm(1,0,servo_min)
pwm.set_pwm(2,0,servo_min)

xdir=5
ydir=5
zdir=5

x=servo_max//2
y=servo_max//2
z=servo_max//2

pwm.set_pwm(0,0,x)
pwm.set_pwm(1,0,y)
pwm.set_pwm(2,0,z)

while(True):
    global xdir
    global ydir
    global zdir
    # Put stuff here
    x=x+xdir
    if(x>servo_max):
        x=servo_max
        xdir=-5
    if(x<servo_min):
        x=servo_min
        xdir=5

    y=y+zdir
    if(y>servo_max):
        y=servo_max
        ydir=-5
    if(y<servo_min):
        y=servo_min
        ydir=5

    z=z+zdir
    if(z>servo_max):
        z=servo_max
        zdir=-5
    if(z<servo_min):
        z=servo_min
        zdir=5

    pwm.set_pwm(0,0,x)
    pwm.set_pwm(1,0,y)
    pwm.set_pwm(2,0,z)        
