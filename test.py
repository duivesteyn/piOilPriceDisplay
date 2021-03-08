#!/usr/bin/env python3
# Simple test code to check it gets the data correctly.

import pprint
import configparser
import boot

def performTestOfDataCollection():

    #intro
    appname = 'piOilPriceDisplay'       
    version = '1.6'
    print('----------------------------\n' + appname + ' ' + version + '\n----------------------------\n')
    print(appname + ": Loading Price Screen")

    #Get Config Info from Settings.yaml file.
    Config = configparser.ConfigParser()
    Config.read("settings.yaml")

    #get Oil Price Data
    newData = boot.getPrice()

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

performTestOfDataCollection()