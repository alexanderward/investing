import os

import datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from stock_apis.api import get_historic, get_listed_companies

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investing.settings")
import django

django.setup()
from app.models import Symbol, SymbolHistory


def get_listed_stocks():
    companies = get_listed_companies()

    def check_fields(name_, sector_, industry_, ipo_year_, market_cap_, symbol_object):
        if symbol_object.company != name_:
            symbol_object.company = name_
        if symbol_object.sector != sector_:
            symbol_object.sector = sector_
        if symbol_object.industry != industry_:
            symbol_object.industry = industry_
        if symbol_object.ipo_year != ipo_year_:
            symbol_object.ipo_year = ipo_year_
        if symbol_object.market_cap != market_cap_:
            symbol_object.market_cap = market_cap_
        return symbol

    all_symbols = set(Symbol.objects.all().values_list('symbol', flat=True))
    current_symbols = set()
    for company in companies:
        symbol_ = company[0]
        name = company[1]
        last_sale = company[2]
        market_cap = None if company[3] == 'n/a' else float(company[3])
        adr_tso = company[4]
        ipo_year = None if company[5] == 'n/a' else int(company[5])
        sector = company[6]
        industry = company[7]
        summary_quote = company[8]

        symbol, created = Symbol.objects.get_or_create(symbol=symbol_)
        symbol = check_fields(name, sector, industry, ipo_year, market_cap, symbol)
        symbol.save()

        current_symbols.add(symbol_)

    for symbol__ in all_symbols.difference(current_symbols):
        symbol = Symbol.objects.get(symbol=symbol__)
        symbol.listed = False
        symbol.save()


def calculate_growth_rate(old_value, new_value, years=5):
    old_value = float(old_value)
    new_value = float(new_value)
    years = float(years)
    ratio = new_value / old_value
    growth_rate = ratio ** (1 / years)
    return float((growth_rate - 1) * 100)


# symbols = Symbol.objects.all()
# now = datetime.datetime.now()
# now_minus_five_years = datetime.datetime(year=now.year - 5, month=now.month, day=now.day)
#
# for symbol in symbols:
#         # Super lazy method ... just drop and write everyday
#         try:
#             historic_data = get_historic(symbol.symbol, now_minus_five_years)
#             if historic_data:
#                 SymbolHistory.objects.filter(symbol=symbol).delete()
#
#             symbol_history_list = []
#             for day in historic_data:
#                 is_bad_data = False
#                 if float(day[6]) > 1000:
#                     is_bad_data = True
#                 symbol_history_list.append(SymbolHistory(
#                     symbol=symbol,
#                     date=day[0],
#                     open=day[1],
#                     high=day[2],
#                     low=day[3],
#                     close=day[4],
#                     volume=day[5],
#                     adj_close=day[6],
#                     is_bad_data=is_bad_data
#                 ))
#             SymbolHistory.objects.bulk_create(symbol_history_list)
#             first_symbol = SymbolHistory.objects.filter(symbol=symbol).order_by('date').first()
#             if first_symbol:
#                 last_symbol = SymbolHistory.objects.filter(symbol=symbol).order_by('date').last()
#                 symbol.growth_rate = calculate_growth_rate(first_symbol.adj_close, last_symbol.adj_close)
#                 symbol.save()
#         except AssertionError:
#             pass


# symbols = Symbol.objects.filter(growth_rate__isnull=False)
# for symbol in symbols:
#     symbol_history = SymbolHistory.objects.filter(symbol=symbol, adj_close__gte=1000)
#     if symbol_history:
#         print symbol, symbol_history.count()


sectors = ['Transportation',
           'Health Care',
           'Basic Industries',
           'Energy',
           'Public Utilities',
           'Consumer Services',
           'Consumer Non-Durables',
           'Technology',
           'Capital Goods',
           'Consumer Durables',
           'Miscellaneous',
           'Finance',
           'n/a']

# for sector in sectors:
#     top_five = Symbol.objects.filter(growth_rate__isnull=False, sector=sector).order_by('-growth_rate')[:5]
#     print sector, zip(sorted([x.growth_rate for x in top_five]), sorted([x.symbol for x in top_five]))

symbols = Symbol.objects.all()
for symbol in symbols:
    symbol_history = SymbolHistory.objects.filter(symbol=symbol, close__isnull=False, close__gt=0).order_by('date')
    if symbol_history:
        symbol_history_minus_first_year = symbol_history.filter(date__year__gt=symbol_history.first().date.year)

        if symbol_history_minus_first_year:
            first_symbol = symbol_history_minus_first_year.first()
            last_symbol = symbol_history_minus_first_year.last()
            years = last_symbol.date.year - first_symbol.date.year
            if years:
                symbol.growth_rate = calculate_growth_rate(first_symbol.close, last_symbol.close, years)
            else:
                symbol.growth_rate = None
            symbol.save()
        else:
            symbol.growth_rate = None
            symbol.save()
    else:
        symbol.growth_rate = None
        symbol.save()

        # get_listed_stocks()
        # symbols = Symbol.objects.all()
        # now = datetime.datetime.now()
        # now_minus_five_years = datetime.datetime(year=now.year - 5, month=now.month, day=now.day)
        #
        # for symbol in symbols:
        #     # Super lazy method ... just drop and write everyday
        #     try:
        #         historic_data = get_historic(symbol.symbol, now_minus_five_years)
        #         if historic_data:
        #             SymbolHistory.objects.filter(symbol=symbol).delete()
        #
        #         symbol_history_list = []
        #         for day in historic_data:
        #             symbol_history_list.append(SymbolHistory(
        #                 symbol=symbol,
        #                 date=datetime.datetime.strptime(day[0], '%d-%b-%y'),
        #                 open=None if '-' in day[1] else day[1],
        #                 high=None if '-' in day[2] else day[2],
        #                 low=None if '-' in day[3] else day[3],
        #                 close=None if '-' in day[4] else day[4],
        #                 volume=None if '-' in day[5] else day[5]
        #             ))
        #         SymbolHistory.objects.bulk_create(symbol_history_list)
        #         first_symbol = SymbolHistory.objects.filter(symbol=symbol, close__isnull=False, close__gt=0).order_by('date').first()
        #         if first_symbol:
        #             last_symbol = SymbolHistory.objects.filter(symbol=symbol, close__isnull=False, close__gt=0).order_by('date').last()
        #             symbol.growth_rate = calculate_growth_rate(first_symbol.close, last_symbol.close)
        #             symbol.save()
        #     except AssertionError:
        #         pass
