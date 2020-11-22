#!/usr/bin/env python3
# coding: utf-8

# duivesteyn // Python // Oil Price Display // getPriceFromProvider
# https://github.com/duivesteyn/piOilPriceDisplay
# little pi zero with epaper display that constantly presents the WTI oil price (Month+1)
#
# 2020-11-22 v2.0
#
#Code Notes
# Function that gets latest oil price data from provider. 
# 
# Rollover Dates:
# https://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude_product_calendar_futures.html

#usage: x = getPrice(oil)
def getPrice (commodity,verbose=0): #default verbose=0

    import datetime
    import requests					#for http GET 
    import json
    
    #Futures Data Source URL Base
    futuresURL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
    querystring = {"symbols":"CL=F","region":"US"} #V2 for rapidAPI
    headers = {
        'x-rapidapi-key': "7092e32bd4msh6843219535bfb0ap1b768bjsn2d2fff2ed657",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    #Settings
    oilString = "CL"
    if(commodity == "oil") : URLprefix = oilString

    #Call URL
    if(verbose): print('Calling URL: ' + futuresURL)
    #r = requests.get(completeURL)
    r = requests.request("GET", futuresURL, headers=headers, params=querystring)

    # if response = 200 then
    if r.status_code==200 : 
    	if(verbose): print(' Data Lookup Succeeded:' + str(r.status_code))
    	data = json.loads(r.content)['quoteResponse']['result'][0]
    	if(verbose): print(data)
    	return data
    else:
        return None