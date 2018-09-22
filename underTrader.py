import numpy as np
import sys
import time
import random
import socket
import json

team_name = 'MANDMANDM'

test_mode = True
test_exchange_index = 0

prod_exchange_hostname = 'production'

port = 25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name})
    hello_res = read_from_exchange(exchange)

    trader(exchange, "AAPL", 0.5)


def trader(exchange, symbol, cooldown):
    t0, t1 = 0, 0
    hist = np.zeros(smooth)
    time_since_last_order = cooldown
    
    while 1:
        time_since_last_order += (t1 - t0)  # * 100
        t0 = time.time()
        message = read_from_exchange(exchange)

        print(message['type'], message)
        print(time_since_last_order)
        print("==============================================")
        
        if(message['book'] and message['symbol'] == symbol):
            trade_id = random.randint(0, 2 ** 32)
            write_to_exchange(exchange, {"type": "add", "order_id": trade_id, "symbol": symbol, "dir": "SELL", "price": message['sell'][0][0] - 1, "size": 1})
            write_to_exchange(exchange, {"type": "add", "order_id": trade_id, "symbol": symbol, "dir": "BUY", "price": message['buy'][0][0] + 1, "size": 1})

        t1 = time.time()


if __name__ == "__main__":
    main()
