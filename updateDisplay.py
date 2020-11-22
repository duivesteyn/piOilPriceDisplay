#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-11-22 v1.2
# 
#
# Prerequisites
# python3, PIL, inkyphat

#Code Notes
# Ideally to be ran every 30 mins and to update a little rpi zero with the current price

#Changelog 
#v1.0 - original release - get price and print in terminal
#v1.1 - Updated Text Size, and rotated 180deg
#v1.2 - API Changed from CME to yahoo finance

# Available Properties 
# "last":"28.01",
# "change":"+0.45"
# "priorSettle":"27.56",
# "open":"27.64",
# "close":"-",
# "high":"28.75"
# "low":"27.24
# "volume":"13,426"
# "percentageChange":"+1.63%"
# "escapedQuoteCode":"CLM0"

#--------------------------------------------------
#|                                     2020-05-23 | 
#|            ____  ___     ___   ___ 		      |
#|           (___ \/ _ \   / __) / __)		      |
#|            / __/\__  )_(  _ \(___ \		      |
#|           (____)(___/(_)\___/(____/            |
#|                                                |
#--------------------------------------------------
import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from inky import InkyPHAT
from getPrice import getPrice                                                                                   #local library from getPrice.py
import pprint

#intro
appname = 'piOilPriceDisplay'       
version = '1.2'
print('----------------------------\n' + appname + ' ' + version + '\n----------------------------\n')
print(appname + ": Loading Price Screen")

#getOilData
newData = getPrice('oil')
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
fontExLg = ImageFont.truetype("elec.ttf", 40) 
fontLg = ImageFont.truetype("elec.ttf", 18  ) 
font = ImageFont.truetype("elec.ttf", 10) 

# Load Strings
strLast = '$' +  str(newData['regularMarketPrice'])
strChange = str(newData['regularMarketChangePercent'])
strH = 'H:' + str(newData['regularMarketDayHigh']) + " "
strL = 'L:' + str(newData['regularMarketDayLow'])  + " "

# Write text                
draw.text((  3,  3), 'OLJEPRISEN' +  "   ", inky_display.BLACK, font=fontLg)
draw.text((141,  1), datetime.today().strftime('%Y-%m-%d')     + "   ", inky_display.BLACK, font=font) 
x=draw.textsize(datetime.today().strftime('%Y-%m-%d'), font)[0]-draw.textsize(datetime.today().strftime('%H:%M'), font)[0]
draw.text((141+x+4, 10), datetime.today().strftime('%H:%M')+ "   ", inky_display.BLACK, font=font)          
draw.text(( 5, 30) , strLast, inky_display.BLACK, font=fontExLg)                                                 #Price, #33.56
draw.text((160, 40), strH  , inky_display.BLACK, font=font)                                                    #High, 34.00
draw.text((160, 50), strL  , inky_display.BLACK, font=font)                                                    #Low,  30.72
xDistanceToStartPercentageChange=1+draw.textsize(strLast, fontExLg)[0]-draw.textsize(strChange, fontLg)[0]-3    #Right Aligning %Change and Last Price
draw.text((xDistanceToStartPercentageChange, 70), str(strChange) + " ", inky_display.BLACK, font=fontLg)        #Change, -5.31%. Right Aligned with the last price
draw.text((1, 94), str(newData['quoteCode']) +" ", inky_display.BLACK, font=font)                               #Footer: CLX

# Write to Display
inky_display.set_border(colour)
inky_display.set_image(img)
inky_display.show()