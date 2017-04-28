import json

from services import IChart, NASDAQ, Google, YahooFinance
from itertools import chain


def get_stock_statistics(symbol):
    yahoo = YahooFinance()
    return yahoo.get_statistics(symbol)


def get_stock_news(symbol):
    yahoo = YahooFinance()
    return yahoo.get_news(symbol)


def get_comments(symbol):
    yahoo = YahooFinance()
    return yahoo.get_comments(symbol)


def get_historic(symbol, from_date):
    ichart = IChart()
    return ichart.get_symbol(symbol, from_date=from_date), '%Y-%m-%d'
    # google = Google()
    # return google.get_symbol(symbol, from_date=from_date), '%d-%b-%y'


def get_listed_companies():
    nasdaq_api = NASDAQ()
    return nasdaq_api.get_nasdaq_companies()
    # return chain(nasdaq_api.get_nasdaq_companies(), nasdaq_api.get_nyse_companies())

    # import datetime
    # now = datetime.datetime.now()
    # now_minus_five_years = datetime.datetime(year=now.year - 5, month=now.month, day=now.day)
    # for x in get_historic('SAB', now_minus_five_years):
    #     print x
    #
    # for x in get_listed_companies():
    #     print x


# data = get_stock_statistics('ATVI'); filename='stats.json'
# # data = get_comments('ATVI'); filename='comments.json'
# # data = get_news('ATVI'); filename='news.json'
# with open(filename, 'w') as f:
#     json.dump(data, f, indent=4, sort_keys=True)
