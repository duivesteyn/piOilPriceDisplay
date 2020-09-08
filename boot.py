#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-05-23 v1.0
#
# LOGIN SCREEN - Optional, but useful when you power on this unit after a year of it sitting in the cupboard. Only goes to price screen if internet is detected
#
#--------------------------------------------------
#|                                     2020-05-23 |
#|            piOilPriceDisplay v1.0              |
#|                                                |
#|    github.com/duivesteyn/piOilPriceDisplay     |
#|                                                | internet: -> internet: OK (if internet works)		
#|        internet:ok         Data:CME            | Data: -> Data:CME         
#--------------------------------------------------
#
# Reference: 
# https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
# https://github.com/pimoroni/inky

import glob
import time
import os
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne
from datetime import datetime
import socket

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 80))
        print("Internet Connection Test Passed")
        return True
    except OSError:
        pass
    return False
    
#strings
appname = "piOilPriceDisplay"
version = "1.1"
url = "github.com/duivesteyn"
datasource= "CME"

PATH = os.path.dirname(__file__) # Get the current path
print(appname + ": Loading Boot Screen")
date=datetime.today().strftime('%Y-%m-%d')

# Set up the display
colour = "black"
inky_display = InkyPHAT(colour)
inky_display.set_border(inky_display.BLACK)
inky_display.v_flip = True
inky_display.h_flip = True

# Create a new canvas to draw on
w, h = 212, 104
img = Image.new("P", (w, h))
#bg
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 0), (w, h)], fill=1, outline=1)

# Draw lines
draw.line((0, 12, w, 12))      # Horizontal top line
draw.line((0, h-12, w, h-12))  # Horizontal bottom line

# Load Font
fontLg = ImageFont.truetype("elec.ttf", 16) 
font = ImageFont.truetype("elec.ttf", 10) 

#Internet Check
connectionTest = is_connected()
if connectionTest == True:
    internetStr="OK" 
else:
    internetStr="Fail" 

# Write text
datetime = time.strftime("%d/%m %H:%M")
draw.text((135, 0), date + "   ", inky_display.WHITE, font=font)
draw.text((5, 22), appname + "  ", inky_display.WHITE, font=fontLg)
draw.text((5,40), "v" + str(version) + "  ", inky_display.WHITE, font=font)
draw.text((5,54), url+ "   ", inky_display.WHITE, font=font)
draw.text((5, 95), "internet:" + internetStr +  "   ", inky_display.WHITE, font=font)
draw.text((120, 95), "Provider:" + datasource + "   ", inky_display.WHITE, font=font)

# Display
inky_display.set_border(colour)
inky_display.set_image(img)
inky_display.show()

#Sleep Boot Screen
print('Starting 5s sleep')
time.sleep(5)
 
#Run main price page if internet is connected
if connectionTest == True:
    print('loading updateDisplay page')
    exec(open('updateDisplay.py').read())
else:
    print('No Internet detected, Staying on Boot Screen')
