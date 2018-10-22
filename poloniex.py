import time
import ujson

import requests

TICKER = "https://poloniex.com/public?command=returnTicker"


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
    poloniex_ticker = get_ticker()
    poloniex_buy_sell = {'name': 'poloniex', 'pairs': {}}
    for pair in poloniex_ticker:
        first_part, second_part = pair.split("_")
        reverse_pair = second_part+"_"+first_part
        poloniex_buy_sell['pairs'][reverse_pair] = {'buy': poloniex_ticker[pair]['lowestAsk'], 'sell': poloniex_ticker[pair]['highestBid']}
    return poloniex_buy_sell