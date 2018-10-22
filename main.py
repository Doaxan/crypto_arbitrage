import itertools
from collections import OrderedDict

import yobit

import exmo
import hitbtc
import poloniex
import binance


def get_profit(ex_buy, ex_sell):
    profit = {}
    for pair in ex_buy:
        try:
            first_part, second_part = pair.split("_")
            if pair in ex_sell:
                if float(ex_buy[pair]['buy']) == 0: continue
                # buy_to_sell_profit = float(ex_sell[pair]['sell']) - float(ex_buy[pair]['buy'])
                buy_to_sell_profit = 100 - (float(ex_buy[pair]['buy'])/float(ex_sell[pair]['sell']) * 100)
                if buy_to_sell_profit < 0: continue
                profit[pair] = {'buy': ex_buy[pair]['buy'], 'sell': ex_sell[pair]['sell'], 'profit': round(buy_to_sell_profit, 2)}
            elif second_part + "_" + first_part in ex_sell:
                reverse_pair = 1 / float(ex_sell[second_part + "_" + first_part]['buy'])
                # buy_to_sell_profit = reverse_pair - float(ex_buy[pair]['buy'])
                buy_to_sell_profit = 100 - (float(ex_buy[pair]['buy']) / reverse_pair*100)
                if buy_to_sell_profit < 0: continue
                profit[pair + "r"] = {'buy': ex_buy[pair]['buy'], 'sell': reverse_pair, 'profit': round(buy_to_sell_profit, 2)}
        except (TypeError, ZeroDivisionError):
            continue

    profit_sorted = OrderedDict(sorted(profit.items(), key=lambda t: t[1]['profit'], reverse=True))
    return profit_sorted


def main():
    # get_info_all()
    exmo_buy_sell = exmo.get_buy_sell()
    hitbtc_buy_sell = hitbtc.get_buy_sell()
    poloniex_buy_sell = poloniex.get_buy_sell()
    binance_buy_sell = binance.get_buy_sell()
    all_exc = (exmo_buy_sell, hitbtc_buy_sell, poloniex_buy_sell, binance_buy_sell)

    # all
    for exc1 in all_exc:
        for exc2 in all_exc:
            if exc1 is exc2: continue
    for exc1, exc2 in itertools.combinations(all_exc, 2):
        print(exc1['name'], 'to', exc2['name'], get_profit(exc1['pairs'], exc2['pairs']))
        print(exc2['name'], 'to', exc1['name'], get_profit(exc2['pairs'], exc1['pairs']))
        print()

    # yobit
    # for exc1 in all_exc:
    #     yobit_exc = yobit.get_buy_sell(exc1['pairs'].keys())
    #     print(exc1['name'], 'to', ' yobit', get_profit(exc1['pairs'], yobit_exc['pairs']))
    #     print('yobit ', 'to', exc1['name'], get_profit(yobit_exc['pairs'], exc1['pairs']))

    # print("exmo to hitbtc", get_profit(exmo_buy_sell['pairs'], hitbtc_buy_sell['pairs']))
    # print("hitbtc to exmo", get_profit(hitbtc_buy_sell['pairs'], exmo_buy_sell['pairs']))
    # print()
    # print("exmo to poloniex", get_profit(exmo_buy_sell['pairs'], poloniex_buy_sell['pairs']))
    # print("poloniex to exmo", get_profit(poloniex_buy_sell['pairs'], exmo_buy_sell['pairs']))
    # print()
    # print("poloniex(r) to hitbtc", get_profit(poloniex_buy_sell['pairs'], hitbtc_buy_sell['pairs']))
    # print("hitbtc to poloniex(r)", get_profit(hitbtc_buy_sell['pairs'], poloniex_buy_sell['pairs']))
    # print()
    # print("exmo to binance", get_profit(exmo_buy_sell['pairs'], binance_buy_sell['pairs']))
    # print("binance to exmo", get_profit(binance_buy_sell['pairs'], exmo_buy_sell['pairs']))
    # print()
    # yobit_buy_sell = yobit.get_buy_sell(exmo_buy_sell.keys())
    # print("exmo to yobit", get_profit(exmo_buy_sell, yobit_buy_sell))
    # print("yobit to exmo", get_profit(yobit_buy_sell, exmo_buy_sell))


if __name__ == "__main__":
    main()
