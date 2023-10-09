import mss
import cv2
import numpy as np
import pytesseract
import pyttsx3
import random

def play_audio() : # text to speech with pyttsx3
    bad_voicelines = ["your a failure", "A fetus could've answered that fucking question", "You should fix your brain"]
    engine = pyttsx3.init()
    engine.say(random.choice(bad_voicelines))
    engine.runAndWait()



while True:

    with mss.mss() as sct :
        monitor_number = 1
        mon = sct.monitors[monitor_number]

        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }

        output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor) 
        # formatting where to screenshot

        # grab the data
        sct_img = sct.grab(monitor) # screenshot
        print('screenshotted')
        img = np.array(sct_img) # holds our screenshot
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


        # white colormask arrays
        sensitivity = 90
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])
            
        # color mask
        mask = cv2.inRange(img_hsv, lower_white, upper_white) # filter out all white colors


        # invert colors so its black on white
        invert_mask = cv2.bitwise_not(mask) # invert the color mask image
        

        # OCR
        imgText = str(pytesseract.image_to_string(invert_mask)).lower()

        if "incorrect" in imgText :
            play_audio()
        

        
