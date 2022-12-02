import requests 
import json 
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
from datetime import timedelta, date, datetime
from pybit import usdt_perpetual
from pybit.usdt_perpetual import HTTP

mode = "test"
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"

# SESSION Activation
session = HTTP(api_url)

def get_all_tickers():
    dict = session.query_symbol()["result"]
    json_object = json.dumps(dict) 
    json_array = json.loads(json_object)
    ticker_list = []
    for symbol in json_array:
                if symbol["quote_currency"] == "USDT" and float(symbol["maker_fee"]) < 0.0002 and symbol["status"] == "Trading":
                    ticker_list.append(symbol["name"])
    print(len(ticker_list))
    print(ticker_list)
    
    return ticker_list

def get_historical_Data(symbol,  interval, startTime, limit):
 
    url = "https://api.bybit.com/v2/public/kline/list"
 
    startTime = str(int(startTime.timestamp()))
    req_params = {"symbol" : symbol, 'interval' : interval, 'from' : startTime, 'limit' : limit}
 
    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text)['result'])
    if len(df) > 0:
        df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time] 
    print(df)
    return df


# Get historical prices (klines)
def get_price_klines(symbol,from_time, interval, limit):
    print((datetime.combine(date.today() - timedelta(days=200), datetime.min.time())))

    # get prices
    prices = pd.DataFrame(session.query_mark_price_kline(
        symbol = symbol,
        interval = interval,
        limit = limit,
        from_time = from_time
    )['result'])
    #prices.index = [dt.datetime.fromtimestamp(x) for x in prices.open_time]


    # Manage API calls
    time.sleep(0.1)
    print(prices)
    return prices



def get_prices_for_200_days():
    ticker_list = get_all_tickers()
    for symbol in ticker_list:
        print(symbol)
        interval = '15'
        limit = '96'
        days = 200
        from_time = (datetime.combine(date.today() - timedelta(days=200), datetime.min.time()))
        print(from_time)
        df_list = []
        for x in range(days):
            new_df = get_price_klines(symbol,int(from_time.timestamp()),interval,limit)
            #new_df = get_historical_Data(symbol, interval, last_datetime, limit)
            if len(new_df) == 0:
                break
            print(new_df)
            df_list.append(new_df)
            from_time += dt.timedelta(days=1)
            df = pd.concat(df_list)
            df.to_csv('200 days data of ' + symbol, index=False)
        #if len(new_df) > 0:
            #tradable_ticker_list.append(symbol)
    return

def continously_update_data():
    tradeable_ticker_list = get_all_tickers()
    get_prices_for_200_days()
    starttime = time.time()
    test_time = datetime.combine(date.today(), datetime.min.time())
    interval = '15'
    limit = '1'
    print("test time:", test_time)
    while True:
        time.sleep(900.0 - ((time.time() - starttime) % 900.0))
        print("tick")
        for symbol in tradeable_ticker_list:
            new_df = get_price_klines(symbol,int(test_time.timestamp()),interval,limit)
            new_df.to_csv('200 days data of ' + symbol, mode='a', index=False, header=False)
            print("Data appended successfully.")
        test_time += dt.timedelta(days=15/(96*15))
        print(tradeable_ticker_list)

continously_update_data()