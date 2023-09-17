#!/usr/bin/env python3

import picamera
from gpiozero import LED, Button
from datetime import datetime
from time import sleep
import signal
import os, sys

"""
A simple script for taking pictures when the camera is attached 
to my stereo microscope

Two buttons and one LED are used:

* trigger button
* stop button
* indicator LED

When the script is started, a preview window is opened. Pressing the
trigger button takes
a picture at the highest resolution.

Needs to be stopped either by pressing the stop button, or by stopping
the python process (CTRL-D, or kill the process in ssh session)

Armin H., 02-2021
"""

RESOLUTION = None   # camera.MAX_RESOLUTION if set to "None". 
                    # (4056, 3040) for hi-res camera
SCREEN_DIMS = (1920, 1080) #  # Dimension of live preview, e.g. (1920,1080)
IMG_LOCATION = '/home/pi/Pictures'

# Set up which pins to use for LED and buttons
led = LED(17)
button = Button(23, bounce_time=.5) # trigger button
button2 = Button(24, hold_time=1) # exit button

# Workaround for using a button to kill the signal.pause()
# https://www.raspberrypi.org/forums/viewtopic.php?t=268903
# Handler for SIGUSER1
def handleSignal(num, stack):
  #print('Got signal! And now we mysteriously will exit....')
  pass # we don't really need to do anything with this, just avoid error mess.

# define the signal:
signal.signal(signal.SIGUSR1, handleSignal)

def blink_led(num_blinks, blink_duration):
    for _ in range(num_blinks):
        led.on()
        sleep(blink_duration)
        led.off()
        sleep(blink_duration)

def take_picture():
    """
    Gets called when button is pressed
    """
    print('Taking a picture!')
    timestamp=datetime.now().isoformat()
    img_name = 'image_'+str(timestamp)+'.jpg'
    img_path = os.path.join(IMG_LOCATION, img_name)
    led.on()
    camera.capture(img_path)
    led.off()
    print('Image saved as : {}'.format(img_path))
    
def stop_program():
    """Close the program to get rid of video overlay"""
    print('Stop button pressed. Exiting...')
    blink_led(6, 0.1)
    os.kill(os.getpid(), signal.SIGUSR1)

print('Starting Simple Microscope Camera')
print('Press trigger button to take photo.')
print('Hold exit button to stop program.')

# set up the camera
camera = picamera.PiCamera()
if not RESOLUTION:
    camera.resolution = camera.MAX_RESOLUTION
else:
    camera.resolution = RESOLUTION
    
# Start the live preview at different resolution:
camera.start_preview(resolution=SCREEN_DIMS, fullscreen=True)

button.when_pressed = take_picture
button2.when_held = stop_program

signal.pause()