#!/usr/bin/env python3

"""
NOT READY YET. GOAL: to use buttons to control the raspberry pi camera 
while it is mounted on my stereo-microscope.

Button 1: Aquire image (photo mode)/ Start video (video mode)
Button 2: Change modes (photo <-> video)
Button 3: Exit program on long press


"""

import os, sys
import signal
import time
from datetime import datetime
import RPi.GPIO as GPIO
import picamera

# Set some camera defaults:
RESOLUTION = None # camera.MAX_RESOLUTION if set to "None". 
                  # max is (4056, 3040) for hi-res camera
SCREEN_DIMS = (1352, 640) # Dimension of live preview, e.g. (1920,1080)
IMG_LOCATION = '/home/pi/Pictures' # where to save images/videos

# set up the the camera        
camera = picamera.PiCamera()
if not RESOLUTION:
    camera.resolution = camera.MAX_RESOLUTION
else:
    camera.resolution = RESOLUTION

# Define button GPIO pin #s
# BCM numbering scheme, see:
# https://learn.sparkfun.com/tutorials/raspberry-gpio/gpio-pinout
BTN_1_PIN = 23 # Trigger button
BTN_2_PIN = 24 # Mode button
BTN_3_PIN = 25 # Exit button
# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mode = 0 # 1 is photo, 1 is video
modenames = {0: 'photo', 1: 'video'}

def take_picture():
    """
    Gets called when trigger button is pressed in photo mode
    """
    timestamp=datetime.now().isoformat()
    img_name = 'image_'+str(timestamp)+'.jpg'
    img_path = os.path.join(IMG_LOCATION, img_name)
    
    # led.on
    camera.capture(img_path)
    # led.off
    
    print('Image saved as : {}'.format(img_path))

def start_video():
    print('Still to implement...')
    pass
    
def stop_video():
    print('Still to implement...')
    pass

def toggle_mode():
    """ 
    Still needs to be implemented"""
    global mode
    if mode:
        mode = 0
    else:
        mode = 1   


# Workaround for using a button to kill the signal.pause()
# https://www.raspberrypi.org/forums/viewtopic.php?t=268903
# Handler for SIGUSER1
def handleSignal(num, stack):
  #print('Got signal! And now we mysteriously will exit....')
  pass # we don't really need to do anything with this, just avoid error mess.

# define the signal:  
signal.signal(signal.SIGUSR1, handleSignal)
        
# callback functions for buttons:
def btn_1_callback(channel):
    global mode
    print('Button press detected on btn 1')
    if mode == 0:
        take_picture()
    if mode == 1:
        if video_in_progress:
            stop_video()
        else:
            start_video()
    
def btn_2_callback(channel):
    global mode
    print('Button press detected on btn 2')
    toggle_mode()
    print('Switched to {} mode'.format( modenames[mode] ) )
    
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
        if ticks > 100:               
            print('Exiting program')
            os.kill(os.getpid(), signal.SIGUSR1)
    
    
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
    # Start the live preview at different resolution:
    camera.start_preview(resolution=SCREEN_DIMS, fullscreen=True)
    
    # GPIO.wait_for_edge(BTN_1_PIN, GPIO.FALLING)
    signal.pause()
    
except KeyboardInterrupt:
    print('')
    print('Exiting program.')
    
GPIO.cleanup()
