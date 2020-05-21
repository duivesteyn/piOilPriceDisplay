#!/usr/bin/python
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-05-16 v1.0
#
# Prerequisites
# python3

#Code Notes
# Ideally to be ran every 30 mins and to update a little rpi zero with the current price

#Changelog 
#v1.0 - original release - get price and print in terminal

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

from getPrice import getPrice


#intro
title = 'duivesteyn/piOilPriceDisplay'       
version = '1.0'
print('----------------------------\n' + title + ' ' + version + '\n----------------------------\n')


#getOilData
newData = getPrice('oil')

#updateDisplay Here
print("Volume " + newData['volume'])

#--------------------------------------------------
#|                                     2020-05-16 | 
#|            ____  ___     ___   ___ 		      |
#|           (___ \/ _ \   / __) / __)		      |
#|            / __/\__  )_(  _ \(___ \		      |
#|           (____)(___/(_)\___/(____/            |
#|                                                |
#--------------------------------------------------