from services import IChart, NASDAQ, Google
from itertools import chain


def get_gain_metrics(daily=False, weekly=False, monthly=False, annually=True):
    pass


def get_historic(symbol, from_date):
    # ichart = IChart()
    # return ichart.get_symbol(symbol, from_date=from_date)
    google = Google()
    return google.get_symbol(symbol, from_date=from_date)


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