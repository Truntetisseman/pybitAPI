import requests 
import json 
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
from datetime import timedelta, date, datetime

from pybit import inverse_perpetual
session_unauth = inverse_perpetual.HTTP(
    endpoint="https://api-testnet.bybit.com"
)
dict = session_unauth.query_symbol()["result"]

json_object = json.dumps(dict) 
json_array = json.loads(json_object)
ticker_list = []
ticker_list = [d['name'] for d in json_array]
print(ticker_list)
ticker_list2 = ['ETHUSD', 'BTCUSD','XRPUSD']
#ticker_list2 = ['BTCUSD']


def get_historical_Data(symbol,  interval, startTime, limit):
 
    url = "https://api.bybit.com/v2/public/kline/list"
 
    startTime = str(int(startTime.timestamp()))
    req_params = {"symbol" : symbol, 'interval' : interval, 'from' : startTime, 'limit' : limit}
 
    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text)['result'])
 
    df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time] 
    print(df)
    return df

for symbol in ticker_list2:
    print(symbol)
    interval = 15
    limit = 96
    days = 200
    last_datetime = (datetime.combine(date.today() - timedelta(days=200), datetime.min.time()))
    print(last_datetime)
    df_list = []
    for x in range(days):
        new_df = get_historical_Data(symbol, interval, last_datetime, limit)
        df_list.append(new_df)
        last_datetime += dt.timedelta(days=1)
    df = pd.concat(df_list)
    df.to_csv('200 days data of ' + symbol, index=False)


starttime = time.time()
test_time = datetime.combine(date.today(), datetime.min.time())
print("test time:", test_time)
print("Heyhy", interval/(limit*interval))
while True:
    time.sleep(900.0 - ((time.time() - starttime) % 900.0))
    print("tick")
    for symbol in ticker_list2:
        new_df = get_historical_Data(symbol, interval, test_time, 1)
        new_df.to_csv('200 days data of ' + symbol, mode='a', index=False, header=False)
        print("Data appended successfully.")
    test_time += dt.timedelta(days=interval/(limit*interval))
    print("test time2:", test_time)