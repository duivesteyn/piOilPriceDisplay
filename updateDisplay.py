#!/usr/bin/env python3
# coding: utf-8
#
# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# Code Notes:
# Run every 10 mins and updates a device with the current price. 

# Draws this display:
#--------------------------------------------------
#|  OILPRICE                           2020-05-23 | 
#|            ____  ___     ___   ___ 		      |
#|           (___ \/ _ \   / __) / __)            |
#|            / __/\__  )_(  _ \(___ \	          |
#|           (____)(___/(_)\___/(____/            |
#|                                                |
#--------------------------------------------------

import boot

def updateDisplay():
    ScreenInfo = boot.setup()
    boot.updateMainScreen(ScreenInfo)

updateDisplay()