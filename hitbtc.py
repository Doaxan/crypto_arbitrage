import time
import ujson

import requests

SYMBOLS = "https://api.hitbtc.com/api/2/public/symbol"
TICKER = "https://api.hitbtc.com/api/2/public/ticker"


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


def get_symbols():
    return request_json(SYMBOLS)


def get_buy_sell():
    hitbtc_ticker = get_ticker()
    hitbtc_symbols = get_symbols()

    # print(hitbtc_symbols)
    # print("exmo:", exmo_ticker)
    # print("hitbtc:", hitbtc_ticker)

    # I buy, I sell
    hitbtc_buy_sell = {'name': 'hitbtc', 'pairs': {}}
    for pair in hitbtc_ticker:
        # print(pair['symbol'])
        for value in hitbtc_symbols:
            if value['id'] == pair['symbol']:
                # print(value['baseCurrency']+"_"+value['quoteCurrency'])
                hitbtc_buy_sell['pairs'][value['baseCurrency'] + "_" + value['quoteCurrency']] = {
                    'buy': pair['ask'], 'sell': pair['bid']}
                break
    return hitbtc_buy_sell
