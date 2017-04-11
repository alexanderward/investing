# import os
#
# import datetime
import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from stock_apis.api import get_historic, get_listed_companies

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investing.settings")
import django

django.setup()
from app.models import Symbol, SymbolHistory

from afinn import Afinn


# afinn = Afinn()
# # text = requests.get("http://finance.yahoo.com/news/videogame-stock-roundup-nintendos-switch-204508012.html")
# # text = requests.get("http://us.rd.yahoo.com/finance/SIG=12q80ki1p/*http%3A//www.fool.com/investing/2017/03/09/3-tech-stocks-to-buy-in-march.aspx?yptr=yahoo")
# # print afinn.score(text.content)
# text = r"""
# Sell this stock now.  Analysts predict steep losses.
# """
# print afinn.score(text)


def get_average_percent_change(symbol, day_count=100):
    historic_days = list(SymbolHistory.objects.filter(symbol=symbol).order_by('date'))[-day_count:]
    percent_changes = []
    for historic_day in enumerate(historic_days):
        index, day = historic_day
        if not day.close or not day.open:
            continue
        percent_change = abs(float(day.close - day.open) / float(day.close) * 100)
        percent_changes.append(percent_change)

    if not percent_changes:
        return None
    return sum(percent_changes) / len(percent_changes)


# symbols = Symbol.objects.all()
# for symbol in symbols:
#     print symbol.symbol, get_average_percent_change(symbol, day_count=20)


print get_average_percent_change(Symbol.objects.get(symbol='IOTS'), day_count=20)

