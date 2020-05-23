#!/usr/bin/python
# coding: utf-8

# duivesteyn // Python // Oil Price Display // getPriceFromProvider
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-05-16 v1.0
#

#Code Notes
# Function that gets latest oil price data from provider. 

#Source Notes:
# CME  Group had an easy to use API
# LINK is : https://www.cmegroup.com/CmeWS/mvc/Quotes/FutureContracts/XNYM/G?quoteCodes=CLM0
#               OIL = CL, M = Month, Year = 0 f0r 2020, 1 for 2021 etc
# 
# Current Month: https://www.cmegroup.com/CmeWS/mvc/Quotes/FutureContracts/XNYM/G?quoteCodes=CLM0
# Typical Response is: {"quoteDelayed":false,"quoteDelay":"-","tradeDate":"15 May 2020","quotes":[{"last":"28.01","change":"+0.45","priorSettle":"27.56","open":"27.64","close":"-","high":"28.75","low":"27.24","highLimit":"-","lowLimit":"-","volume":"13,426","mdKey":"CLM0-XNYM-G","quoteCode":"CLM0","escapedQuoteCode":"CLM0","code":"-","updated":"05:51:35 CT<br /> 15 May 2020","percentageChange":"+1.63%","expirationMonth":"-","expirationCode":"-","expirationDate":"-","productName":"-","productCode":"-","uri":"-","productId":"-","exchangeCode":"XNYM","optionUri":"-","hasOption":false,"lastTradeDate":"-","priceChart":"-","netChangeStatus":"statusOK","highLowLimits":"No Limit / No Limit"}],"empty":false}
# 
# Rollover Dates:
# https://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude_product_calendar_futures.html

#usage: x = getPrice(oil)
def getPrice (commodity):

    import datetime
    import requests					#for http GET 
    import pprint
    import json
    
    #Futures Data Source URL Base
    futuresURL = "https://www.cmegroup.com/CmeWS/mvc/Quotes/FutureContracts/XNYM/G?quoteCodes="

    # Futures Month Codes
    # Ref https://www.cmegroup.com/month-codes.html
    # ---------------------------
    #Month		Month Code
    #January	F
    #February	G
    #March		H
    #April		J
    #May		K
    #June		M -> CLM2020 for the month. ask this 1 month ahead.
    #July		N
    #August		Q
    #September	U
    #October	V
    #November	X
    #December	Z
    futureMonths=['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'] #Array for Holding futures. Jan=0, Feb=1, Mar=2, Dec=11 etc.

    # Available Properties 
    # ---------------------------
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

    #Settings
    oilString = "CL"
    if(commodity == "oil") : URLprefix = oilString
    
    #Get Date
    dt = datetime.datetime.today()

    #Contract expires generally around 20th of month, so if Day Of Month > 20, go to the next months contract! 
    dom = dt.day
    if(dom > 19): monthRollover = 1
    
    #Date Slicing for correct month contract URL.
    URLyear = str(dt.year)[-1:]                     #Get last digit of year
    month = dt.month + monthRollover				#Jan=1, Dec=12
    
    if(month > 11): month = month - 12				#adjust for december back to 0!
    URLmonth = str(futureMonths[month])				#want 1 month advance, but the array is -1, so its +1-1 = month


    #Build URL for CME Exchange
    #https://www.cmegroup.com/CmeWS/mvc/Quotes/FutureContracts/XNYM/G?quoteCodes=CL + MONTHCHAR + FINAL DIGIT OF YEAR
    completeURL = futuresURL + URLprefix + URLmonth + URLyear
    
    #Call URL
    print('Calling URL: ' + completeURL)
    r = requests.get(completeURL)
    exchangeOutput = json.loads(r.content)

    # if response = 200 then
    if r.status_code==200 : 
    	#pprint.pprint(exchangeOutput)
    	print(' Data Lookup Succeeded:' + str(r.status_code))
    	#Delve into the  JSON
    	items = exchangeOutput['quotes']
    	data = items[0]
    	return data
    else:
        return None