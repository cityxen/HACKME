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
#######################################################################################
from __future__ import division
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
print('Initializing...')
# Servo initialization stuff
pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
# Configure min and max servo pulse lengths
servo_min = 150 # 150 # Min pulse length out of 4096
servo_max = 600 # 600 # Max pulse length out of 4096
pwm.set_pwm_freq(60)# Set frequency to 60hz, good for servos.
# GPIO initialization stuff
GPIO.setmode(GPIO.BOARD) # Up, Down, left, right, fire
chan_list = [7,11,13,15,16]
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Joystick initialization stuff
fire  = False
up    = False
down  = False
left  = False
right = False
# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def readJoystick():
    global fire
    fire = False
    global up
    up = False
    global down
    down = False
    global left
    left = False
    global right
    right = False
    if(not(GPIO.input(7))):
        fire  = True
    if(not(GPIO.input(11))):
        up    = True
    if(not(GPIO.input(13))):
        down  = True
    if(not(GPIO.input(15))):
        left  = True
    if(not(GPIO.input(16))):
        right = True

pwm.set_pwm(0,0,servo_min)
pwm.set_pwm(1,0,servo_min)
pwm.set_pwm(2,0,servo_min)
time.sleep(2)

x=servo_max//2;
y=servo_max//2;
z=servo_max//2;

while True:
    readJoystick()
    if(fire):
        print('FIRE!')
        z=z+20
        if(z>servo_max):
            z=servo_min
    if(right):
        x=x+5
        if(x>servo_max):
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
    pwm.set_pwm(0,0,x)
    pwm.set_pwm(1,0,y)
    pwm.set_pwm(2,0,z)
    time.sleep(.02)
