import time
import ujson

import requests

TICKER = "https://api.exmo.me/v1/ticker/"


def request_json(url):
    global json_response
    while True:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            json_response = ujson.loads(r.content.decode('utf-8'))
        except ValueError:
            print("error request_json:")
            print(url)
            print(r)
            time.sleep(2)
            continue
        return json_response


def get_ticker():
    return request_json(TICKER)


def get_buy_sell():
    exmo_ticker = get_ticker()
    exmo_buy_sell = {'name': 'exmo', 'pairs': {}}
    for pair in exmo_ticker:
        exmo_buy_sell['pairs'][pair] = {'buy': exmo_ticker[pair]['sell_price'], 'sell': exmo_ticker[pair]['buy_price']}
    return exmo_buy_sell
