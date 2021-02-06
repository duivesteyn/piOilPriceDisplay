#!/usr/bin/env python3
# Test for non pi device.

import time
import pprint
from datetime import datetime

import piOilPriceDisplay

def performTest():

    #intro
    appname = 'piOilPriceDisplay'       
    version = '1.5'
    print('----------------------------\n' + appname + ' ' + version + '\n----------------------------\n')
    print(appname + ": Loading Price Screen")

    #get Oil Price Data
    newData = piOilPriceDisplay.getPrice()

    pprint.pprint(newData)
    print('------')

    # Load Strings
    strLast = str("%.2f" % newData['regularMarketPrice'])                                                           #Convert float to 2 digit with "%.2f" % float
    strH    = str("%.2f" % newData['high'])
    strL    = str("%.2f" % newData['low'])
    strQuoteCode = newData['underlyingSymbol']
    changeValue = newData['regularMarketChangePercent']
    strChange = str("%.2f" % changeValue)

    print(strLast,strH,strL,strQuoteCode,changeValue,strChange)
    print('Tests Passed!')
    testResult = True

    return testResult

performTest()