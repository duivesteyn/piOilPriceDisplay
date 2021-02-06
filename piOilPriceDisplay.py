#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
# MAIN CLASS, which prints Price to Terminal and sends cleaned data to screen updating classes
#
# Prerequisites
# python3, bmdOilPriceFetch

import sys
import pprint
import bmdOilPriceFetch

#---------------------------------------------------------------------------
# printPrice
# Prints to terminal -> python3 printPrice.py
# usage: printPrice()
#---------------------------------------------------------------------------
def printPrice():

    data = bmdOilPriceFetch.bmdPriceFetch()
    outputString = 'The price of WTI is $' + str("%.2f" % data['regularMarketPrice'])
    print(outputString)
    
    return outputString
    
#---------------------------------------------------------------------------
# getPrice
# Function that sends sanitised marketdata and adds HIGH/LOW price into dict
# usage: x = getPrice()
# 
# 
# OUTPUT
# =======
# {
# 'Ask': 52.73,
# 'Bid': 52.72,
# "Day's Range": '50.81 - 52.74',
# 'Last Price': 50.83,
# 'Open': 50.93,
# 'Pre. Settlement': nan,
# 'Quote Price': 52.709999084472656,
# 'Settlement Date': '2021-01-20',
# 'Volume': 460177.0}
# 'underlyingSymbol': 'CL=F', 
# 'regularMarketChange': 1.850000305175783, 
# 'regularMarketChangePercent': 3.6395835238555634, 
# 'Low': '50.81', 
# 'High': '52.74'
# }
#---------------------------------------------------------------------------
def getPrice(verbose=0): #default verbose=0

    ticker='CL=F' #WTI Front Month from CME/YahooFinance
    
    marketData = bmdOilPriceFetch.bmdPriceFetch(ticker)

    if marketData:
        
        #Add Underlying Symbol into Data
        marketData['underlyingSymbol'] = ticker
        
        #Bring in Change amount (without leading + sign or % sign) 
        #in v1.5 this is possible from comparing the lastClose and the current price.
        marketData['regularMarketChange'] =marketData['regularMarketPrice'] - marketData['lastClose']
        marketData['regularMarketChangePercent'] = marketData['regularMarketChange']/marketData['lastClose']*100
        
        return marketData
    
if __name__ == "__main__":
    printPrice()