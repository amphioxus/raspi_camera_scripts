import picamera
from gpiozero import LED, Button
from datetime import datetime
from signal import pause
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

Armin H., 2021
"""

RESOLUTION = None   # camera.MAX_RESOLUTION if set to "None". 
                    # (4056, 3040) for hi-res camera
SCREEN_DIMS = (1352, 640) #  # Dimension of live preview, e.g. (1920,1080)
IMG_LOCATION = '/home/pi/Pictures'
# Set up which pins to use for LED and buttons
led = LED(17)
button = Button(18) # trigger button
button2 = Button(24) # exit button


def take_picture():
    """
    Gets called when button is pressed
    """
    timestamp=datetime.now().isoformat()
    img_name = 'image_'+str(timestamp)+'.jpg'
    img_path = os.path.join(IMG_LOCATION, img_name)
    
    led.on        
    camera.capture(img_path)
    led.off
    
    print('Image saved as : {}'.format(img_path))

def stop_program():
    """Close the program to get rid of video overlay"""
    print('Stop button pressed')
    sys.exit(0)
    
# set up the camera        
camera = picamera.PiCamera()
if not RESOLUTION:
    camera.resolution = camera.MAX_RESOLUTION
else:
    camera.resolution = RESOLUTION
    
# Start the live preview at different resolution:
camera.start_preview(resolution=SCREEN_DIMS, fullscreen=True)

button.when_pressed = take_picture
button2.when_pressed = stop_progam

pause()
