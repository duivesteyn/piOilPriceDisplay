#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
# MAIN CLASS, which prints Price to Terminal and sends cleaned data to screen updating classes
#
# 2021-01-09 v1.0
#
# Prerequisites
# python3

import sys
import pprint

import stock_info

#---------------------------------------------------------------------------
# printPrice
# Prints to terminal -> python3 printPrice.py
# usage: printPrice()
#---------------------------------------------------------------------------
def printPrice():
   
    marketData =  getPrice()
    outputString = 'The price of WTI is $' + str("%.2f" % marketData['Quote Price'])

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
    
    marketData = stock_info.get_quote_table(ticker)
    
    if marketData:
        
        #Add Underlying Symbol into Data
        marketData['underlyingSymbol'] = ticker
        
        #Bring in Change amount (without leading + sign or % sign) 
        #in v1.3 this is possible from comparing the LAST price and the current price.
        marketData['regularMarketChange'] = changeAmount=(marketData['Quote Price'] - marketData['Last Price'])
        marketData['regularMarketChangePercent'] = marketData['regularMarketChange']/marketData['Last Price']*100
    
        #Seperate High and Low from Yahoos "Day's Range" into the Market Data Dictionary
        if marketData[ "Day's Range"]:
            txtStr=marketData[ "Day's Range"].split('-')
            marketData['Low']= float(txtStr[0].strip())
            marketData['High']= float(txtStr[1].strip())
    
            return marketData
    

if __name__ == "__main__":
    printPrice()
    
    
