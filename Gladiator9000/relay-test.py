##########################################################################################
# CityXen 16 Relay Board Test Program
# by Deadline
#
# NOTE: This is subject to heavy modification, especially the way it converts the signals
# so don't presume that the state it is in now is the way it will stay
#
# Raspberry Pi (Any model with 40 GPIO should work)
# https://amzn.to/34X5Xnj
#
# The Serial connector board is a MAX3232 based mini board with a 9 pin dsub
# https://amzn.to/32G9Viv
#
# Null modem required to work with Amiga serial port
# https://amzn.to/32BrHDC
#
# 8 Channel Relay Board
# https://amzn.to/2Xwerh4
#
# Prototype Wiring
# https://amzn.to/2LHDNX9
#
# GPIO Pins used for the serial device
#
# Pin 6  Ground
# Pin 8  TXD
# Pin 10 RXD
# Pin 1  3 volt
#
# GPIO Pins used for the Relay Boards
#
# Pin 4  5 volt VCC Relay Board 1
# Pin 6  Ground Relay Board 1
#
# Relay Board 1 relays
#
# Pin 37 Relay 1
# Pin 35 Relay 2
# Pin 33 Relay 3
# Pin 31 Relay 4
# Pin 29 Relay 5
# Pin 23 Relay 6
# Pin 21 Relay 7
# Pin 19 Relay 8
#
# Relay Board 2
#
# Pin 15 Relay 1
# Pin 13 Relay 2
# Pin 11 Relay 3
# Pin 7  Relay 4
# Pin 12 Relay 5
# Pin 16 Relay 6
# Pin 18 Relay 7
# Pin 22 Relay 8
#
# Relay Board 3
#
# Pin 40 Relay 1
# Pin 38 Relay 2
# Pin 36 Relay 3
# Pin 32 Relay 4
#
##########################################################################################

import RPi.GPIO as GPIO
import time
import argparse

# Set up some variables
test_version    = "1.0"

print("CityXen Gladiator 9000 Relay Test version %s" % (test_version))

# Set up a dictionary for GPIO pins used for the relay up/down states
#gp = {12:False, 7:False,11:False,13:False,15:False,19:False,21:False,23:False,16:False,18:False,22:False,40:False,38:False,36:False,32:False,37:False}
gp2= {37:False,35:False,33:False,31:False,29:False,23:False,21:False,19:False}
gp3= {15:False,13:False,11:False,7:False,12:False,16:False,18:False,22:False}
gp4= {40:False,38:False,36:False,32:False}

# Set up GPIO device
GPIO.setwarnings(True) # Ignore some warnings
GPIO.setmode(GPIO.BOARD)
#for i in gp:    GPIO.setup(i, GPIO.OUT) # Set pins to out
for i in gp2:
    GPIO.setup(i, GPIO.OUT) # Set pins to out
for i in gp3:
    GPIO.setup(i, GPIO.OUT) # Set pins to out
for i in gp4:
    GPIO.setup(i, GPIO.OUT) # Set pins to out

# Define some functions
def set_gpio(): # Set the GPIO pins from dict values
    global gp2
    global gp3
    global gp4
    #for i in gp:        GPIO.output(i,gp[i])
    for i in gp2:
        GPIO.output(i,gp2[i])
    for i in gp3:
        GPIO.output(i,gp3[i])
    for i in gp4:
        GPIO.output(i,gp4[i])


def all_on(): # Turn all dict values to on
    global gp2
    global gp3
    global gp4
    #for i in gp:   gp[i]=False
    for i in gp2:
        gp2[i]=False
    for i in gp3:
        gp3[i]=False
    for i in gp4:
        gp4[i]=False

def all_off(): # Turn all dict values to off
    global gp2
    global gp3
    global gp4
    #for i in gp:        gp[i]=True
    for i in gp2:
        gp2[i]=True
    for i in gp3:
        gp3[i]=True
    for i in gp4:
        gp4[i]=True

def test_sequence(): # Turn on and off all dict values and then set the GPIO pins
    global gp2
    global gp3
    global gp4
    for i in gp2:
	print(i)
        gp2[i]=False
        set_gpio()
        time.sleep(2)
        gp2[i]=True
        set_gpio()
    for i in gp3:
	print(i)
        gp3[i]=False
        set_gpio()
        time.sleep(2)
        gp3[i]=True
        set_gpio()
    for i in gp4:
	print(i)
        gp4[i]=False
        set_gpio()
        time.sleep(2)
        gp4[i]=True
        set_gpio()

# Do or do not, there is no try...
#if(init_test):
print("Running Relay Board Test")
test_sequence() # Do a quick system test

# Turn off all GPIO pins
all_off()
set_gpio()

# GPIO.cleanup()

