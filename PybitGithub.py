from time import sleep
from pybit import inverse_perpetual
from pybit import spot

ws_inverse = inverse_perpetual.WebSocket(
    test=True
)

def handle_orderbook(message):
    print(message)
    orderbook_data = message["data"]

ws_inverse.orderbook_25_stream(handle_orderbook, ["BTCUSD"])

while True:
    sleep(1)