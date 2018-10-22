import sys
import time
import ujson

import requests

TICKER = "https://yobit.io/api/3/ticker/"
INFO = "https://yobit.io/api/3/info"
TRADES = "https://yobit.io/api/3/trades/"


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


def get_method_all(all_pairs, method, limit=25):
    # print("Start get_pairs")
    all_pairs_method = {}
    counter = 0
    counter_all = 0
    result = method
    for pair in all_pairs:
        # print(pair)
        result = result + pair + '-'
        counter += 1
        counter_all += 1
        if counter > limit:
            print('\r', 'method:', method, "[", counter_all, "/", len(all_pairs), "]", end='')
            sys.stdout.flush()

            result = result[:-1]
            result = result + "?ignore_invalid=1"
            # print("RESULT1:")
            # print(result)
            req = request_json(result)
            all_pairs_method.update(req)

            # print(counter)
            counter = 0
            result = method
            time.sleep(0.6)
    if result != method:
        result = result[:-1]
        result = result + "?ignore_invalid=1"
        # print("RESULT2:")
        # print(result)
        req = request_json(result)
        all_pairs_method.update(req)

    print('\r', end='')
    sys.stdout.flush()
    return all_pairs_method


def get_all_pairs():
    return request_json(INFO)['pairs']


def get_ticker(ticker_pairs):
    ticker_pairs = list(ticker_pairs)
    for i, pair in enumerate(ticker_pairs):
        # for exmo
        first_part, second_part = pair.split("_")
        if second_part == 'RUB':
            second_part = 'RUR'
            pair_new = first_part+"_"+second_part
            ticker_pairs[i] = pair_new
    ticker_pairs = {x.lower() for x in ticker_pairs}
    all_pairs_ticker = get_method_all(ticker_pairs, TICKER)
    return all_pairs_ticker


def get_buy_sell(ticker_pairs):
    yobit_ticker = get_ticker(ticker_pairs)
    yobit_buy_sell = {'name': 'yobit', 'pairs': {}}
    for pair in yobit_ticker:
        # for exmo
        first_part, second_part = pair.split("_")
        name = pair.upper()
        if second_part == 'rur':
            second_part = 'rub'
            name = (first_part+"_"+second_part).upper()
        yobit_buy_sell['pairs'][name] = {'buy': yobit_ticker[pair]['sell'], 'sell': yobit_ticker[pair]['buy']}
    return yobit_buy_sell
