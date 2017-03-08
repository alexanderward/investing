import datetime
from celery.schedules import crontab
from celery.task import periodic_task

from celery.utils.log import get_task_logger

from robinhood import RobinHood
from creds import get_robinhood_creds

from app.models import User, Financial, Symbol, SymbolHistory
from stock_apis.api import get_listed_companies, get_historic

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour='8-17', day_of_week="mon-fri")))  # , minute="*/5")))
def get_user_financials():
    email = 'alexander.ward1@gmail.com'
    logger.info("Starting: Getting financials for %s" % email)
    user = User.objects.get(email=email)
    rh = RobinHood()
    if not user.rh_token:
        username, password = get_robinhood_creds()
        assert rh.login(username, password)
    else:
        rh.api_token = "Token %s" % user.rh_token
    balance = rh.get_account_balance()
    Financial.objects.create(user=user,
                             available_funds=balance.get('available_funds'),
                             funds_held_for_orders=balance.get('funds_held_for_orders'),
                             portfolio_value=balance.get('value'))
    logger.info("Finished: Getting financials for %s" % email)


@periodic_task(run_every=(crontab(day_of_week="mon-fri")))  # every minute m-f
def get_user_positions():
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


@periodic_task(run_every=(crontab(hour='1', day_of_week="mon-fri")))  # every minute m-f
def get_listed_stocks():
    logger.info("Starting: Getting all listed stocks for NASDAQ")
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

    logger.info("Completed: Getting all listed stocks for NASDAQ")


@periodic_task(run_every=(crontab(hour='3', day_of_week="mon-fri")))  # every minute m-f
def get_symbol_history():
    def calculate_growth_rate(old_value, new_value, years=5):
        old_value = float(old_value)
        new_value = float(new_value)
        years = float(years)
        ratio = new_value / old_value
        growth_rate = ratio ** (1 / years)
        return float((growth_rate - 1) * 100)

    logger.info("Starting: Getting all listed stocks historical stocks")
    symbols = Symbol.objects.all()
    now = datetime.datetime.now()
    now_minus_five_years = datetime.datetime(year=now.year - 5, month=now.month, day=now.day)

    for symbol in symbols:
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
                    open=day[1],
                    high=day[2],
                    low=day[3],
                    close=day[4],
                    volume=day[5],
                ))
            SymbolHistory.objects.bulk_create(symbol_history_list)
            symbol_history = SymbolHistory.objects.filter(symbol=symbol, close__isnull=False, close__gt=0).order_by(
                'date')
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
        except AssertionError:
            pass
    logger.info("Completed: Getting all listed stocks historical stocks")