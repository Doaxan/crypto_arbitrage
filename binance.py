import time
import ujson

import requests

SYMBOLS = "https://api.binance.com/api/v1/exchangeInfo"
TICKER = "https://api.binance.com/api/v3/ticker/bookTicker"


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
    binance_ticker = get_ticker()
    binance_symbols = get_symbols()['symbols']

    # print(hitbtc_symbols)
    # print("exmo:", exmo_ticker)
    # print("hitbtc:", hitbtc_ticker)

    # I buy, I sell
    binance_buy_sell = {'name': 'binance', 'pairs': {}}
    for pair in binance_ticker:
        # print(pair['symbol'])
        for value in binance_symbols:
            if value['symbol'] == pair['symbol']:
                # print(value['baseCurrency']+"_"+value['quoteCurrency'])
                binance_buy_sell['pairs'][value['baseAsset'] + "_" + value['quoteAsset']] = {
                    'buy': pair['askPrice'], 'sell': pair['bidPrice']}
                break

    return binance_buy_sell
