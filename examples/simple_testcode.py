#Low Power Mosfet v1.0p test code

from machine import Pin
from pyb import CAN, Timer
import utime


print("starting Low Power Mosfet test")
print("v1.0")
print("initializing")
can = CAN(1, CAN.NORMAL)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))


#Setup Pins
HBT_LED = Pin("D5", Pin.OUT)
FUNC_BUTTON = Pin("E7", Pin.IN, Pin.PULL_UP) 
NEO_STATUS = Pin("E6", Pin.OUT)
can_wakeup = Pin("D6", Pin.OUT)
can_wakeup.value(0)

BUTTON_1 = Pin("E12", Pin.IN, Pin.PULL_UP) 
BUTTON_2 = Pin("E11", Pin.IN, Pin.PULL_UP) 
BUTTON_3 = Pin("E10", Pin.IN, Pin.PULL_UP) 

FET_1 = Pin("E3", Pin.OUT) #Timer 12, Chan 1 
FET_2 = Pin("D0", Pin.OUT) #Timer 2, Chan 4   
FET_3 = Pin("D1", Pin.OUT) #Timer 2, Chan 3
    
TIMER_12 = Timer(12, freq=1000) 
TIMER_2 = Timer(2, freq=1000)

FET_1_DUTY = TIMER_12.channel(1, Timer.PWM, pin=FET_1)
FET_2_DUTY = TIMER_2.channel(4, Timer.PWM, pin=FET_2)
FET_3_DUTY = TIMER_2.channel(3, Timer.PWM, pin=FET_3)

    
    
    
    #Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
HBT_LED.value(hbt_state)


print("starting")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            HBT_LED.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            HBT_LED.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

      

def send():
    can.send('lowPrFET', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
    simple_test()

def simple_test():
    print("starting test")
    for i in range(50):
        FET_1_DUTY.pulse_width_percent(i*2)
        utime.sleep_ms(10)
    for i in range(50):
        FET_1_DUTY.pulse_width_percent(100-(i*2))
        utime.sleep_ms(10)
    FET_1_DUTY.pulse_width_percent(0)
    for i in range(50):
        FET_2_DUTY.pulse_width_percent(i*2)
        utime.sleep_ms(10)
    for i in range(50):
        FET_2_DUTY.pulse_width_percent(100-(i*2))
        utime.sleep_ms(10)
    FET_2_DUTY.pulse_width_percent(0)
    for i in range(50):
        FET_3_DUTY.pulse_width_percent(i*2)
        utime.sleep_ms(10)
    for i in range(50):
        FET_3_DUTY.pulse_width_percent(100-(i*2))
        utime.sleep_ms(10)
    FET_3_DUTY.pulse_width_percent(0)

while True:
    chk_hbt()
    if not (FUNC_BUTTON.value()):
        print("function button")
        send()
        simple_test()
        utime.sleep_ms(200)
    
    if(can.any(0)):
        get()
    
    if not (BUTTON_1.value()):
        print("BUTTON_1 button")
        for i in range(50):
            FET_1_DUTY.pulse_width_percent(i*2)
            utime.sleep_ms(15)
        for i in range(50):
            FET_1_DUTY.pulse_width_percent(100-(i*2))
            utime.sleep_ms(15)
        FET_1_DUTY.pulse_width_percent(0)
    if not (BUTTON_2.value()):
        print("BUTTON_2 button")
        for i in range(50):
            FET_2_DUTY.pulse_width_percent(i*2)
            utime.sleep_ms(15)
        for i in range(50):
            FET_2_DUTY.pulse_width_percent(100-(i*2))
            utime.sleep_ms(15)
        FET_2_DUTY.pulse_width_percent(0)
    if not (BUTTON_3.value()):
        print("BUTTON_3 button")
        for i in range(50):
            FET_3_DUTY.pulse_width_percent(i*2)
            utime.sleep_ms(15)
        for i in range(50):
            FET_3_DUTY.pulse_width_percent(100-(i*2))
            utime.sleep_ms(15)
        FET_3_DUTY.pulse_width_percent(0)
        
        