#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-11-22 v2.0
#
# Prerequisites
# python3

#Code Notes
# Prints to terminal

# Available Properties 

# "language":"en-US"
# "region":"US"
# "quoteType":"FUTURE"
# "triggerable":false
# "headSymbolAsString":"CL=F"
# "contractSymbol":false
# "currency":"USD"
# "marketState":"REGULAR"
# "underlyingSymbol":"CLF21.NYM"
# "underlyingExchangeSymbol":"CLF21.NYM"
# "openInterest":427104
# "expireDate":1608508800
# "expireIsoDate":"2020-12-21T00:00:00Z"
# "fiftyDayAverage":39.908855
# "fiftyDayAverageChange":2.5611458
# "fiftyDayAverageChangePercent":0.064174876
# "twoHundredDayAverage":38.764088
# "twoHundredDayAverageChange":3.7059135
# "twoHundredDayAverageChangePercent":0.09560172
# "sourceInterval":30
# "exchangeDataDelayedBy":30
# "exchangeTimezoneName":"America/New_York"
# "exchangeTimezoneShortName":"EST"
# "gmtOffSetMilliseconds":-18000000
# "esgPopulated":false
# "tradeable":false
# "firstTradeDateMilliseconds":967003200000
# "regularMarketChange":0.5699997
# "regularMarketChangePercent":1.3603811
# "regularMarketTime":1605909599
# *** "regularMarketPrice":42.47 ***
# "regularMarketDayHigh":42.54
# "regularMarketDayRange":"41.61 - 42.54"
# "regularMarketDayLow":41.61
# "regularMarketVolume":263618
# "regularMarketPreviousClose":41.9
# "bid":42.42
# "ask":42.6
# "bidSize":9
# "askSize":8
# "exchange":"NYM"
# "market":"us24_market"
# "fullExchangeName":"NY Mercantile"
# "shortName":"Crude Oil Jan 21"
# "regularMarketOpen":41.88
# "averageDailyVolume3Month":339797
# "averageDailyVolume10Day":234997
# "fiftyTwoWeekLowChange":82.79
# "fiftyTwoWeekLowChangePercent":-2.0533235
# "fiftyTwoWeekRange":"-40.32 - 65.65"
# "fiftyTwoWeekHighChange":-23.18
# "fiftyTwoWeekHighChangePercent":-0.35308453
# "fiftyTwoWeekLow":-40.32
# "fiftyTwoWeekHigh":65.65
# "priceHint":2
# "symbol":"CL=F"


from getPrice import getPrice                  #local library from getPrice.py
verbose = 0                                    #allows for enabling verbose mode to see whats going on or debugging
textStringFromSourceForLast = 'regularMarketPrice'

#Get the Data from the getPrice module.
newData = getPrice('oil',verbose)                                  
if verbose: pprint.pprint(newData)
if len(newData)>0:
    print('The price of WTI is $' + str(newData[textStringFromSourceForLast]))