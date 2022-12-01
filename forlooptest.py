import requests 
import json 
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
from datetime import timedelta, date, datetime
from pybit import inverse_perpetual

def get_all_tickers():
    session_unauth = inverse_perpetual.HTTP(
         endpoint="https://api-testnet.bybit.com")
    dict = session_unauth.query_symbol()["result"]
    json_object = json.dumps(dict) 
    json_array = json.loads(json_object)
    ticker_list = []
    ticker_list = [d['name'] for d in json_array]
    
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

def get_prices_for_200_days():
    ticker_list = get_all_tickers()
    tradable_ticker_list = []
    for symbol in ticker_list:
        print(symbol)
        interval = 15
        limit = 96
        days = 2
        last_datetime = (datetime.combine(date.today() - timedelta(days=200), datetime.min.time()))
        print(last_datetime)
        df_list = []
        for x in range(days):
            new_df = get_historical_Data(symbol, interval, last_datetime, limit)
            if len(new_df) == 0:
                break
            df_list.append(new_df)
            last_datetime += dt.timedelta(days=1)
            df = pd.concat(df_list)
            df.to_csv('200 days data of ' + symbol, index=False)
        if len(new_df) > 0:
            tradable_ticker_list.append(symbol)
    return tradable_ticker_list

def continously_update_data():
    tradeable_ticker_list = get_prices_for_200_days()
    starttime = time.time()
    test_time = datetime.combine(date.today(), datetime.min.time())
    interval = 15
    limit = 96
    print("test time:", test_time)
    print("Heyhy", interval/(limit*interval))
    while True:
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        print("tick")
        for symbol in tradeable_ticker_list:
            new_df = get_historical_Data(symbol, interval, test_time, 1)
            new_df.to_csv('200 days data of ' + symbol, mode='a', index=False, header=False)
            print("Data appended successfully.")
        test_time += dt.timedelta(days=interval/(limit*interval))
        print(tradeable_ticker_list)

continously_update_data()