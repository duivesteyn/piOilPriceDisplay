#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
#  v1.2
# 
#
# Prerequisites
# python3, PIL, inkyphat

#Code Notes
# Ran every x mins and updates little rpi zero with the current price

# Draws this display:
#--------------------------------------------------
#|  OILPRICE                           2020-05-23 | 
#|            ____  ___     ___   ___ 		      |
#|           (___ \/ _ \   / __) / __)	HHHH      |
#|            / __/\__  )_(  _ \(___ \	LLLL      |
#|           (____)(___/(_)\___/(____/            |
#|                                                |
#--------------------------------------------------

#Changelog 
#v1.0 2020-05-23 - original release - get price and print in terminal
#v1.1 2020-09-04 - Updated Text Size, and rotated 180deg
#v1.2 2020-11-22 - API Changed from CME to yahoo finance
#v1.3 2021-01-08 - API Changed to use Yahoo Finance Directly

import time
import pprint
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from inky import InkyPHAT

import piOilPriceDisplay

#intro
appname = 'piOilPriceDisplay'       
version = '1.4'
print('----------------------------\n' + appname + ' ' + version + '\n----------------------------\n')
print(appname + ": Loading Price Screen")

#Configuration
mainHeaderText = 'OLJEPRISEN' 

#get Oil Price Data
newData = piOilPriceDisplay.getPrice()

pprint.pprint(newData)

#Set up the display
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
draw.rectangle([(0, 0), (w, h)], fill=0, outline=0)                                                             #White=0, Black=1
              
# Draw lines
draw.line((0,   20, w,   20), fill=1)                                                                           #Horizontal top line 
draw.line((0, h-12, w, h-12), fill=1)                                                                           #Horizontal bottom line            

# Load Font
fontExLg = ImageFont.truetype("_resources/elec.ttf", 40) 
fontLg = ImageFont.truetype("_resources/elec.ttf", 18  ) 
font = ImageFont.truetype("_resources/elec.ttf", 10) 

# Load Strings
strLast = str("%.2f" % newData['Quote Price'])                                                           #Convert float to 2 digit with "%.2f" % float
strH    = str("%.2f" % newData['High'])
strL    = str("%.2f" % newData['Low'])
strQuoteCode = newData['underlyingSymbol']
changeValue = newData['regularMarketChangePercent']

#TxtModification
strChange = str("%.2f" % changeValue)
if(changeValue>0) : strChange = "+" + strChange

# Write text
draw.text((  3,  3), mainHeaderText +  "   ", inky_display.BLACK, font=fontLg)
draw.text((141,  1), datetime.today().strftime('%Y-%m-%d')     + "   ", inky_display.BLACK, font=font) 
x=draw.textsize(datetime.today().strftime('%Y-%m-%d'), font)[0]-draw.textsize(datetime.today().strftime('%H:%M'), font)[0]
draw.text((141+x+4, 10), datetime.today().strftime('%H:%M')+ "   ", inky_display.BLACK, font=font)          
draw.text(( 5, 30) , '$' + strLast, inky_display.BLACK, font=fontExLg)                                          #Price, 33.56
draw.text((160, 40), 'H' + strH + ' ' , inky_display.BLACK, font=font)                                          #High,  34.00
draw.text((160, 50), 'L' + strL + ' ' , inky_display.BLACK, font=font)                                          #Low,   30.72
xDistanceToStartPercentageChange=1+10+draw.textsize(strLast, fontExLg)[0]-draw.textsize(strChange, fontLg)[0]    #Right Aligning %Change and Last Price
draw.text((xDistanceToStartPercentageChange, 70), strChange + "% ", inky_display.BLACK, font=fontLg)            #Change, -5.31%. Right Aligned with the last price
draw.text((1, 94), strQuoteCode +" ", inky_display.BLACK, font=font)                                            #Footer: CLX

# Write to Display
inky_display.set_border(colour)
inky_display.set_image(img)
inky_display.show()