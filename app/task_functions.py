import datetime
from celery.utils.log import get_task_logger
from django.db import transaction

from app.models import SymbolHistory, Financial, Symbol
from robinhood import RobinHood
from stock_apis.api import get_listed_companies, get_historic

logger = get_task_logger(__name__)


def get_user_financials(user):
    rh = RobinHood()
    if user.rh_token:
        logger.info("Starting: Getting financials for %s" % user.email)
        rh.api_token = "Token %s" % user.rh_token
        balance = rh.get_account_balance()
        Financial.objects.create(user=user,
                                 available_funds=balance.get('available_funds'),
                                 funds_held_for_orders=balance.get('funds_held_for_orders'),
                                 portfolio_value=balance.get('value'))
        logger.info("Finished: Getting financials for %s" % user.email)


def get_user_positions(user):
    pass
    # email = 'alexander.ward1@gmail.com'
    # logger.info("Starting: Getting financials for %s" % email)
    # user = User.objects.get(email=email)
    # rh = RobinHood()
    # if not user.rh_token:
    #     username, password = get_robinhood_creds()
    #     assert rh.login(username, password)
    # else:
    #     rh.api_token = user.rh_token
    # positions = rh.get_positions()
    # [{u'account': u'https://api.robinhood.com/accounts/5RY40845/',
    #   u'average_buy_price': u'56.5200',
    #   u'created_at': u'2017-02-17T18:33:02.718556Z',
    #   u'instrument': u'https://api.robinhood.com/instruments/09bc1a2d-534d-49d4-add7-e0eb3be8e640/',
    #   u'intraday_average_buy_price': u'0.0000',
    #   u'intraday_quantity': u'0.0000',
    #   u'quantity': u'2.0000',
    #   u'shares_held_for_buys': u'0.0000',
    #   u'shares_held_for_sells': u'2.0000',
    #   u'updated_at': u'2017-02-17T20:30:29.555872Z',
    #   u'url': u'https://api.robinhood.com/accounts/5RY40845/positions/09bc1a2d-534d-49d4-add7-e0eb3be8e640/'},
    # ]
    # logger.info("Finished: Getting positions for %s" % email)


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


@transaction.atomic
def get_symbol_history(symbol):
    def calculate_growth_rate(old_value, new_value, years_=5):
        old_value = float(old_value)
        new_value = float(new_value)
        years_ = float(years_)
        ratio = new_value / old_value
        growth_rate = ratio ** (1 / years_)
        return float((growth_rate - 1) * 100)

    now = datetime.datetime.now()
    now_minus_five_years = datetime.datetime(year=now.year - 5, month=now.month, day=now.day)

    # Super lazy method ... just drop and write everyday
    try:
        historic_data = get_historic(symbol.symbol, now_minus_five_years)
        if historic_data:
            SymbolHistory.objects.filter(symbol=symbol).delete()

        symbol_history_list = []
        for day in historic_data:
            symbol_history_list.append(SymbolHistory(
                symbol=symbol,
                date=datetime.datetime.strptime(day[0], '%d-%b-%y'),
                open=None if day[1] == '-' else day[1],
                high=None if day[2] == '-' else day[2],
                low=None if day[3] == '-' else day[3],
                close=None if day[4] == '-' else day[4],
                volume=None if day[5] == '-' else day[5],
            ))
        SymbolHistory.objects.bulk_create(symbol_history_list)
        symbol_history = SymbolHistory.objects.filter(symbol=symbol, open__isnull=False, close__isnull=False,
                                                      close__gt=0).order_by('date')

        if symbol_history:
            most_recent = symbol_history.last()
            symbol.last_open = most_recent.open
            symbol.last_close = most_recent.close
            if most_recent.volume and symbol.average_volume:
                avg_volume = float((float(symbol.average_volume) + float(most_recent.volume)) / 2)
            else:
                avg_volume = most_recent.volume
            symbol.average_volume = avg_volume
            symbol_history_minus_first_year = symbol_history.filter(date__year__gt=symbol_history.first().date.year)

            if symbol_history_minus_first_year:
                first_symbol = symbol_history_minus_first_year.first()
                last_symbol = symbol_history_minus_first_year.last()
                years = last_symbol.date.year - first_symbol.date.year
                if years:
                    symbol.growth_rate = calculate_growth_rate(first_symbol.close, last_symbol.close, years)
                else:
                    symbol.growth_rate = None
            else:
                symbol.growth_rate = None
        else:
            symbol.growth_rate = None
    except AssertionError:
        pass
    return symbol


def get_average_percent_change(symbol, day_count=100):
    historic_days = SymbolHistory.objects.filter(symbol=symbol).order_by('date')[:day_count]
    percent_changes = []
    for historic_day in enumerate(historic_days):
        index, day = historic_day
        if not day.close or not day.open:
            continue
        percent_change = abs(float(day.close - day.open) / float(day.close) * 100)
        percent_changes.append(percent_change)

    if percent_changes:
        moving_average = sum(percent_changes) / len(percent_changes)
        symbol.moving_average = moving_average
    return symbol
