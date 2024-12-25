import time
import machine
from machine import Pin,Timer,PWM
led = Pin(25, Pin.OUT)
timer = Timer()

#def blink(timer):
#timer.init(freq=10, mode=Timer.PERIODIC, callback=blink)

# Initialize GPIO pins
  # pwm0 = PWM(Pin(0), freq=2000, duty_u16=32768)
#r_en = PWM(Pin(0), freq=1000, duty_u16=1000)
#l_en = PWM(Pin(1), freq=1000, duty_u16=1000)
r_en = machine.Pin(0, machine.Pin.OUT) # WHITE
l_en = machine.Pin(1, machine.Pin.OUT) # BROWN
# rpwm = machine.Pin(2, machine.Pin.OUT) # YELLOW
# lpwm = machine.Pin(3, machine.Pin.OUT) # ORANGE
r_pwm = PWM(Pin(2), freq=1000, duty_u16=1000)
l_pwm = PWM(Pin(3), freq=1000, duty_u16=1000)



# Set motor direction and speed
def set_motor(direction, speed):
    led.toggle()
    time.sleep(1)
    if direction == 'forward':
        r_en.high()
        l_en.low()
    elif direction == 'backward':
        r_en.low()
        l_en.high()        
    r_pwm.freq(speed)
    l_pwm.freq(speed)

# Example usage
x=0
while x < 2:
    x+=1
    set_motor('forward', 1000)  # Move motor forward at 1000 Hz
    set_motor('backward', 1000)

    
led.off()




