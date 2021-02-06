#!/usr/bin/env python3

import os, sys
from signal import pause
import time
import RPi.GPIO as GPIO

# Define button pin #s
# BCM numbering scheme, see:
# https://learn.sparkfun.com/tutorials/raspberry-gpio/gpio-pinout
BTN_1_PIN = 23
BTN_2_PIN = 24
BTN_3_PIN = 25
# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# callback functions:
def btn_1_callback(channel):
    print('Button press detected on btn 1')
    
def btn_2_callback(channel):
    print('Button press detected on btn 2')
    
def btn_3_callback(channel):
    """
    Count how long button is in pressed state.
    If long enough, exit program.
    """
    ticks = 0
    # print('Button press detected on btn 3')
    while GPIO.input(channel) == 0: # Wait for the button up
        ticks += 1
        time.sleep(0.01)   
    # print('Ticks: {}'.format(ticks))
    if ticks > 100:               
        print('Exiting program')        
        GPIO.cleanup()
        sys.exit(0)
    else:
        pass
        # print('Not pressed long enough')
    
    
GPIO.add_event_detect(  BTN_1_PIN, 
                        GPIO.RISING, 
                        callback = btn_1_callback,
                        bouncetime = 300)    
GPIO.add_event_detect(  BTN_2_PIN, 
                        GPIO.RISING, 
                        callback = btn_2_callback,
                        bouncetime = 300)      
GPIO.add_event_detect(  BTN_3_PIN, 
                        GPIO.FALLING, 
                        callback = btn_3_callback,
                        bouncetime = 300)     

try:
    print('waiting')
    # GPIO.wait_for_edge(BTN_1_PIN, GPIO.FALLING)
    pause()
    # print('event detected')
except KeyboardInterrupt:
    print('')
    print('Exiting program.')
    
GPIO.cleanup()
