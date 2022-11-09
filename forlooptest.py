import requests 
import json 
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

def get_historical_Data(symbol,  interval, startTime, limit):
 
    url = "https://api.bybit.com/v2/public/kline/list"
 
    startTime = str(int(startTime.timestamp()))
    req_params = {"symbol" : symbol, 'interval' : interval, 'from' : startTime, 'limit' : limit}
 
    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text)['result'])
 
    df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time]
    print(df)

    return df   

df_list = []
symbol = "BTCUSD"
interval = 15
limit = 96
days = 200
last_datetime = dt.datetime(2022, 4, 22)
for x in range(days):
    print(last_datetime)
    new_df = get_historical_Data(symbol, interval, last_datetime, limit)
    df_list.append(new_df)
    last_datetime += dt.timedelta(days=1)
df = pd.concat(df_list)
df.to_csv('200 days data of ' + symbol, index=False)