#!/usr/bin/env python3
# coding: utf-8
#
# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# An epaper display that constantly presents the WTI oil price
#
# This is the startup script which is all that needs to be ran.
# Pre-requisites, PIL, requests_html, bmdOilPriceFetch, configparser, inky (if using inkyPHAT)
#
# OPTIONS:                      Res
# Waveshare Screen              296x128
# InkyPhat Screen               212x104
# Terminal Only (if on macOS)

import time,os
import random
import sys
import configparser
import logging
import socket
import pprint
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps    

import bmdOilPriceFetch

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#strings
version = "1.6"
appname = "piOilPriceDisplay"
url = "github.com/duivesteyn"
datasource= "Y!"
logging.info( appname + ' ' + version)

#Get Config Info from Settings.yaml file.
Config = configparser.ConfigParser()
Config.read("settings.yaml")

############################################################
## INIT CODE - SETS UP SCREEN TYPE
############################################################
def setup():

    #Object for screendata
    ScreenInfo = {}
    ScreenInfo['screen'] = Config.get('Setup', 'ScreenType')

    #Get Specific Screen Parameters 
    screenSelect(ScreenInfo)
    pprint.pprint(ScreenInfo)

    return ScreenInfo

############################################################
## SHOW BOOT IMAGE
############################################################
def showBootScreen(ScreenInfo):

    #Create Image of Boot Screen for Selected ScreenType
    bootImg = createBootImg(ScreenInfo)

    #Present Screen on Selected Screen  
    if ScreenInfo['screen'] == "waveshare":
        presentOnWaveshareScreen(bootImg)  
    elif ScreenInfo['screen'] == "inky":
        presentOnInkyScreen(bootImg)   
    elif ScreenInfo['screen'] == "terminal":
        presentInTerminal(bootImg) 

    #Sleep to allow time for Boot Screen to persist, then go to Main Screen
    logging.info('Starting 5s sleep')
    time.sleep(5)
    updateMainScreen(ScreenInfo)

############################################################
## SET SPECIFIC SCREENTYPE DATA
############################################################
def screenSelect(ScreenInfo):
    #------------------------------------
    # WAVESHARE 2.9" SCREEN SETUP
    #------------------------------------
    if ScreenInfo['screen'] == "waveshare":
        ScreenInfo['resolution'] =  (296,128)

    #------------------------------------
    # INKY PHAT SCREEN SETUP
    #------------------------------------
    elif ScreenInfo['screen'] == "inky":
        ScreenInfo['resolution'] =  (212,104)
    #------------------------------------
    # RUN IN TERMINAL
    #------------------------------------
    elif ScreenInfo['screen'] == "terminal":
        ScreenInfo['resolution'] =  (296,128)

############################################################
## UPDATE MAIN IMAGE
############################################################
def updateMainScreen(ScreenInfo):
    ''' Function to show Main Screen with Price information onto ePaper Screen. This function is seperate as its all that needs to be ran to update the screen routinely.'''

    #Check Internet Connection
    connectionTest = is_connected()

    if connectionTest:
        mainImg = createSingleStockViewImg(ScreenInfo)
        
        #Present Screen on Selected Screen  
        if ScreenInfo['screen'] == "waveshare":
            presentOnWaveshareScreen(mainImg)  
        elif ScreenInfo['screen'] == "inky":
            presentOnInkyScreen(mainImg)   
        elif ScreenInfo['screen'] == "terminal":
            presentInTerminal(mainImg) 

############################################################
## GENERATION OF BOOT IMAGE
############################################################
def createBootImg(ScreenInfo):

    # Drawing on the Horizontal image
    logging.info(appname + ": Loading Boot Screen")
    inputResolution = ScreenInfo['resolution']

    imgScreen = Image.new('1', inputResolution, 0)
    draw = ImageDraw.Draw(imgScreen)

    w = inputResolution[0]
    h = inputResolution[1]

    #Canvas Colours  0 = black, 1 = white
    bgColor = 0                 
    drawingColor = 1  

    # Create a new canvas to draw on
    draw.rectangle([(0, 0), inputResolution], fill=bgColor,width=0)

    # Draw lines
    draw.line((0, 14, w, 14),fill=drawingColor)                                                             # Horizontal top line
    draw.line((0, h-14, w, h-14),fill=drawingColor)                                                         # Horizontal bottom line

    # Load Font
    fontLg = ImageFont.truetype("_resources/elec.ttf", 16) 
    font = ImageFont.truetype("_resources/elec.ttf", 10) 

    #Internet Check
    connectionTest = is_connected()
    if connectionTest:
        internetStr="OK" 
    else:
        internetStr="Fail" 

    #String Lengths for Right Justified Values
    dateString = datetime.today().strftime('%Y-%m-%d') + " "
    widthOfDate = draw.textsize(dateString,font=font)
    providerString = "Provider:" + datasource + " "
    widthOfProvider = draw.textsize(providerString,font=font)

    # Write text
    draw.text((w-widthOfDate[0]-12, 2), dateString, font=font, fill = drawingColor)                         #Had to rework these for color.
    draw.text((5, 22), appname + "  ", font=fontLg, fill = drawingColor)
    draw.text((5,40), "v" + str(version) + "  ",  font=font, fill = drawingColor)
    draw.text((5,54), url+ "   ",  font=font, fill = drawingColor)
    draw.text((5, h-11), "internet:" + internetStr +  "   ",  font=font, fill = drawingColor)
    draw.text((w-widthOfProvider[0]-5, h-11), providerString,  font=font, fill = drawingColor)

    return imgScreen

############################################################
## GENERATION OF SINGLE STOCK VIEW IMAGE 
############################################################
def createSingleStockViewImg(ScreenInfo):

    mainHeaderText = Config.get('Stocks', 'Choice1Name') #'OLJEPRISEN' 
    newData = getPrice()                                                                                    #get Oil Price Data
    pprint.pprint(newData)
    #newData['regularMarketPrice'] = 100.20                                                                 #For testing >$100 oil

    # Load Strings
    dateString = datetime.today().strftime('%Y-%m-%d')
    timeString = datetime.today().strftime('%H:%M')+ "  "
    strDateTime = dateString + " " + timeString
    strLast = str("%.2f" % newData['regularMarketPrice'])                                                   #Convert float to 2 digit with "%.2f" % float 

    #Canvas
    inputResolution = ScreenInfo['resolution']
    w = inputResolution[0]
    h = inputResolution[1]

    imgScreen = Image.new('1', inputResolution, color=1)
    draw = ImageDraw.Draw(imgScreen)

    #Setup Relative Dimensions #WAVESHARE
    if ScreenInfo['screen'] == 'waveshare' or ScreenInfo['screen'] == 'terminal' :
        iconsize = round(0.62*h)
        headerSize = 25
        footerSize = 13
        spacerH = round(headerSize/5)
        fontExLgFontSize = 50
        fontLgFontSize = 26
        fontFontSize = 10
        txtLine3ChangeYCoord = headerSize+spacerH+fontExLgFontSize
        spacerAdjustmentW = 0
        spacerAdjustmentH = 0
    else:    #INKY
        headerSize = 20
        footerSize = 13
        spacerH = round(headerSize/5)
        if newData['regularMarketPrice']>100:
            iconsize = 52
            fontExLgFontSize = 38
        else:
            iconsize = 60
            fontExLgFontSize = 40
        fontLgFontSize = 18
        fontFontSize = 10
        spacerAdjustmentW=-4
        spacerAdjustmentH=+4
        txtLine3ChangeYCoord = headerSize+spacerH+fontExLgFontSize+spacerAdjustmentH

    # Add in Barrel Icon
    iconName = Config.get('Stocks', 'Choice1Icon') #was "_resources/petrol-barrel.png" 
    icon = Image.open("_resources/" + iconName)                                                             #Load Icon 
    icon = icon.resize((iconsize, iconsize))                                                                #Resize

    #bg
    bgColor = 1           
    drawingColor = 0
    draw.rectangle([(0, 0), (w-1, h-1)], fill=bgColor, outline=0)     

    # Draw lines
    imgScreen.paste(icon, (1, headerSize + spacerH+spacerAdjustmentH))
    draw.line((0,   headerSize, w,   headerSize), fill=drawingColor)                                        #Horizontal top line 
    draw.line((0, h-footerSize, w, h-footerSize), fill=drawingColor)                                        #Horizontal bottom line            

    # Load Resources
    fontExLg = ImageFont.truetype("_resources/elec.ttf", fontExLgFontSize) 
    fontLg = ImageFont.truetype("_resources/elec.ttf", fontLgFontSize) 
    font = ImageFont.truetype("_resources/elec.ttf", fontFontSize)  

    strQuoteCode = newData['underlyingSymbol']+ " "                                                        #inky likes a little extra space at the end.
    changeValue = newData['regularMarketChangePercent']

    #TxtModification
    strChange = str("%.2f" % changeValue)
    if(changeValue>0) : strChange = "+" + strChange
    widthOfDateTime = draw.textsize(strDateTime,font=font) #String Lengths for Right Justified Values

    # Header
    draw.text((3,  2), mainHeaderText +  "   ", font=fontLg, fill=drawingColor)

    #Body
    draw.text((iconsize+spacerAdjustmentW, headerSize+spacerH+spacerAdjustmentH) , '$' + strLast, font=fontExLg, fill=drawingColor)             #Price, 33.56
    xDistance = iconsize+(w-iconsize - draw.textsize(strChange, fontLg)[0] )/2-10                           #Centering of Change%
    draw.text((xDistance, txtLine3ChangeYCoord), strChange + "% ", font=fontLg, fill=drawingColor)          #Change%, -5.31%.

    #Footer
    draw.text((3, h-footerSize+2), strQuoteCode, font=font, fill=drawingColor)                              #Footer: CL=F
    draw.text((w-widthOfDateTime[0], h-footerSize+2), strDateTime , font=font, fill=drawingColor)           #Footer: DateTime

    return imgScreen

############################################################
## GET PRICE DATA
############################################################
def getPrice(ticker='CL=F',verbose=0): #default verbose=0 #Default CL=F is WTI Front Month from CME/YahooFinance

    marketData = bmdOilPriceFetch.bmdPriceFetch(ticker)
    if marketData:
        marketData['underlyingSymbol'] = ticker                                                             #Add Underlying Symbol into Data
        marketData['regularMarketChange'] = marketData['regularMarketPrice'] - marketData['lastClose']      #Bring in Change amount (without leading + sign or % sign) 
        marketData['regularMarketChangePercent'] = marketData['regularMarketChange']/marketData['lastClose']*100        
    else:
        marketData['regularMarketPrice'] = 0
        marketData['regularMarketChangePercent'] = 0
        marketData['underlyingSymbol'] = ticker  

    return marketData

############################################################
## SHOW IMAGE IN TERMINAL
############################################################
def presentInTerminal(image):
    logging.info("Loading Views in terminal using ImageDraw")
    randomNumber = random.randrange(100) 

    filename = "img" + str(randomNumber) + ".png"
    image.show()                                                                                             #Opens the image. 
    image.save(filename)                                                                                    #Save the image to a PNG file called tmp.png.
    os.system("open " + filename)                                                                           #Will open in Preview.
    logging.info("View Sent to Terminal Successfully")

############################################################
## SHOW IMAGE ON INKY PHAT SCREEN  - Pimoroni Inky pHAT (ePaper/eInk/EPD) Black/White SKU: CE06382 (212x104 pixels)
############################################################
def presentOnInkyScreen(image):
    logging.info("Loading View onto Inky Phat.")
    from inky import InkyPHAT
        
    #Test invert image.
    image = image.convert('L')
    image = ImageOps.invert(image)
    image = image.convert('1')

    # Set up the display
    inky_display = InkyPHAT("black")
    #inky_display.set_border(inky_display.BLACK)
    inky_display.v_flip = True
    inky_display.h_flip = True

    # Display
    inky_display.set_border("black")
    inky_display.set_image(image)
    inky_display.show()
    logging.info("View Sent to Device Successfully")

############################################################
## SHOW IMAGE ON WAVESHARE SCREEN - 2.9inch E-Ink display module, SPI interface (296 x128 pixels)
############################################################
def presentOnWaveshareScreen(image):
    logging.info("Loading View onto Waveshare Screen")
    from lib import epd2in9_V2    
    
    #Set up the display
    epd = epd2in9_V2.EPD()
    epd.init()
    #epd.Clear(0xFF)

    # Display
    epd.display(epd.getbuffer(image))
    logging.info("View Sent to Device Successfully")

############################################################
## AUX - TEST FOR INTERNET CONNECTION
############################################################
def is_connected():
    try:                                                                                                    #Connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("1.1.1.1", 80))
        logging.info("Internet Connection Test Passed")
        return True
    except OSError:
        pass
    return False

# Code for First Run
if __name__ == '__main__':
    ScreenInfo = setup()
    showBootScreen(ScreenInfo)