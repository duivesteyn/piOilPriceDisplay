#Originally from https://github.com/atreadw1492/yahoo_fin
#Modified and simplified for yahoo finance commoddity lookup 

import requests
import pandas as pd
import ftplib
import io
import re
import json
import pprint
try:
    from requests_html import HTMLSession
except Exception:
    print("""Warning - Certain functionality 
             requires requests_html, which is not installed.
             
             Install using: 
             pip install requests_html
             
             After installation, you may have to restart your Python session.""")

    
base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"

def build_url(ticker, start_date = None, end_date = None, interval = "1d"):
    
    if end_date is None:  
        end_seconds = int(pd.Timestamp("now").timestamp())
        
    else:
        end_seconds = int(pd.Timestamp(end_date).timestamp())
        
    if start_date is None:
        start_seconds = 7223400    
        
    else:
        start_seconds = int(pd.Timestamp(start_date).timestamp())
    
    site = base_url + ticker
    
    #"{}/v8/finance/chart/{}".format(self._base_url, self.ticker)
    
    params = {"period1": start_seconds, "period2": end_seconds,
              "interval": interval.lower(), "events": "div,splits"}
    
    
    return site, params


def force_float(elt):
    
    try:
        return float(elt)
    except:
        return elt
    


def get_data(ticker, start_date = None, end_date = None, index_as_date = True,
             interval = "1d"):
    '''Downloads historical stock price data into a pandas data frame.  Interval
       must be "1d", "1wk", or "1mo" for daily, weekly, or monthly data.
    
       @param: ticker
       @param: start_date = None
       @param: end_date = None
       @param: index_as_date = True
       @param: interval = "1d"
    '''
    
    if interval not in ("1d", "1wk", "1mo"):
        raise AssertionError("interval must be of of '1d', '1wk', or '1mo'")
    
    # build and connect to URL
    site, params = build_url(ticker, start_date, end_date, interval)
    resp = requests.get(site, params = params)
    
    
    if not resp.ok:
        raise AssertionError(resp.json())
        
    
    # get JSON response
    data = resp.json()

    # get open / high / low / close data
    frame = pd.DataFrame(data["chart"]["result"][0]["indicators"]["quote"][0])

    # add in adjclose
    frame["adjclose"] = data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    
    # get the date info
    temp_time = data["chart"]["result"][0]["timestamp"]
    
    
    frame.index = pd.to_datetime(temp_time, unit = "s")
    frame.index = frame.index.map(lambda dt: dt.floor("d"))
    
    
    frame = frame[["open", "high", "low", "close", "adjclose", "volume"]]
        
    frame['ticker'] = ticker.upper()
    
    if not index_as_date:  
        frame = frame.reset_index()
        frame.rename(columns = {"index": "date"}, inplace = True)
        
    return frame


def get_quote_table(ticker , dict_result = True): 
    
    '''Scrapes data elements found on Yahoo Finance's quote page 
       of input ticker
    
       @param: ticker
       @param: dict_result = True
    '''

    site = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker
    
    tables = pd.read_html(site)

    data = tables[0].append(tables[1])

    data.columns = ["attribute" , "value"]

    price_etc = [elt for elt in tables][0]
        
    price_etc.columns = data.columns.copy()
    
    data = data.append(price_etc)
    
    quote_price = pd.DataFrame(["Quote Price", get_live_price(ticker)]).transpose()
    quote_price.columns = data.columns.copy()
    
    data = data.append(quote_price)
    
    data = data.sort_values("attribute")
    
    data = data.drop_duplicates().reset_index(drop = True)
    
    data["value"] = data.value.map(force_float)

    if dict_result:
        
        result = {key : val for key,val in zip(data.attribute , data.value)}
        return result
        
    return data    



def get_live_price(ticker):
    
    '''Gets the live price of input ticker
    
       @param: ticker
    '''    
    
    df = get_data(ticker, start_date = pd.Timestamp.today() - pd.DateOffset(10), end_date = pd.Timestamp.today() + pd.DateOffset(10))

    return df.close[-1]



    
