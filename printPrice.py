#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-06-01 v1.0
#
# Prerequisites
# python3

#Code Notes
# Prints to terminal

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

from getPrice import getPrice                  #local library from getPrice.py
import pprint
verbose = 0                                    #allows for enabling verbose mode to see whats going on or debugging

#Get the Data from the getPrice module.
newData = getPrice('oil',verbose)                                  
if verbose: pprint.pprint(newData)
if len(newData)>0:
    print('The price of WTI is $' + str(newData['last']))