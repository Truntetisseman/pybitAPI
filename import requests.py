import json
import numpy as np 

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