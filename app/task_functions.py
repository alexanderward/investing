import datetime
import pprint

import operator
import requests
from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Q

debug = True
if debug:
    import sys, os

    sys.path.append('/path/to/your/django/app')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'investing.settings'
    import django

    django.setup()
from app.models import SymbolHistory, Financial, Symbol, SymbolOfficers, SymbolProfile, SymbolNews, Link, User, \
    RobinHoodTransaction, RobinHoodTransactionExecutions, RobinHoodPositions
from robinhood import RobinHood
from stock_apis.api import get_listed_companies, get_historic, get_stock_statistics, get_stock_news
from bulk_update.helper import bulk_update
from afinn import Afinn

logger = get_task_logger(__name__)


class UserFinances(object):
    @staticmethod
    def get_user_balance(user):
        if user.rh_token:
            rh = RobinHood()
            logger.info("Starting: Getting financials for %s" % user.email)
            rh.api_token = "Token %s" % user.rh_token
            balance = rh.get_account_balance()
            Financial.objects.create(user=user,
                                     available_funds=balance.get('available_funds'),
                                     funds_held_for_orders=balance.get('funds_held_for_orders'),
                                     portfolio_value=balance.get('value'))
            logger.info("Finished: Getting financials for %s" % user.email)

    @staticmethod
    @transaction.atomic()
    def retrieve_user_positions(user):
        if user.rh_token:
            rh = RobinHood()
            logger.info("Starting: Getting financials for %s" % user.email)
            rh.api_token = "Token %s" % user.rh_token
            positions = rh.get_positions()
            RobinHoodPositions.objects.filter(user=user).delete()
            new_positions = []
            for position in positions:
                if float(position.get('quantity')):
                    try:
                        symbol = Symbol.objects.get(rh_href=position.get('instrument'))
                    except Symbol.DoesNotExist:
                        results = rh.GET(position.get('instrument'))
                        if results.status_code == 200:
                            symbol_name = results.json()['symbol']
                            symbol = Symbol.objects.create(symbol=symbol_name)
                        else:
                            raise ValueError(
                                'Unable to retrieve %s. Status code: %s' % (position.get('instrument'),
                                                                            results.status_code))
                    rh_position = RobinHoodPositions.objects.create(
                        user=user,
                        symbol=symbol,
                        quantity=position.get('quantity'),
                        created_at=position.get('created_at'),
                        updated_at=position.get('updated_at'),
                        average_buy_price=position.get('average_buy_price')
                    )
                    new_positions.append(rh_position)
            return new_positions

    @staticmethod
    def get_user_positions(user):
        return RobinHoodPositions.objects.filter(user=user)

    @staticmethod
    def get_user_positions_for_symbol(user, symbol):
        if isinstance(symbol, basestring):
            symbol = Symbol.objects.get(symbol=symbol)
        return RobinHoodPositions.objects.filter(user=user, symbol=symbol)

    @staticmethod
    @transaction.atomic()
    def retrieve_user_transactions_from_rh(user):
        if user.rh_token:
            rh = RobinHood()
            logger.info("Starting: Getting financials for %s" % user.email)
            rh.api_token = "Token %s" % user.rh_token
            transactions = rh.get_transactions()
            instrument_links = transactions.keys()
            db_map = Symbol.objects.filter(rh_href__in=instrument_links).values_list('symbol', 'rh_href')

            lookup_table = dict()

            for symbol, rh_href, in db_map:
                lookup_table[rh_href] = symbol

            final_dict = dict()
            lookup_table_reverse = dict()
            for instrument_link, records in transactions.iteritems():
                symbol = lookup_table.get(instrument_link, None)
                if not symbol:
                    results = rh.GET(instrument_link)
                    if results.status_code == 200:
                        symbol = results.json()['symbol']
                    else:
                        raise ValueError(
                            'Unable to retrieve %s. Status code: %s' % (instrument_link, results.status_code))
                final_dict[symbol] = records
                lookup_table_reverse[symbol] = instrument_link

            symbol_updates = []
            for transaction_symbol, transactions in final_dict.iteritems():
                symbol, created = Symbol.objects.get_or_create(symbol=transaction_symbol)
                symbol.rh_href = lookup_table_reverse[transaction_symbol]
                symbol_updates.append(symbol)

                for transaction_instance in transactions:
                    rh_transaction, created = RobinHoodTransaction.objects.get_or_create(
                        user=user,
                        symbol=symbol,
                        created_at=transaction_instance.get('created_at'),
                        rh_id=transaction_instance.get('id'),
                        average_price=transaction_instance.get('average_price'),
                        cumulative_quantity=transaction_instance.get('cumulative_quantity'),
                        state=transaction_instance.get('state'),
                        price=transaction_instance.get('price'),
                        quantity=transaction_instance.get('quantity'),
                        stop_price=transaction_instance.get('quantity'),
                        side=transaction_instance.get('side'),
                        type=transaction_instance.get('type')
                    )
                    for execution in transaction_instance.get('executions'):
                        execution, created = RobinHoodTransactionExecutions.objects.get_or_create(
                            rh_transaction=rh_transaction,
                            symbol=symbol,
                            user=user,
                            rh_id=execution.get('id'),
                            quantity=execution.get('quantity'),
                            price=execution.get('price'),
                            settlement_date=execution.get('settlement_date'),
                            timestamp=execution.get('timestamp')
                        )
            bulk_update(symbol_updates, batch_size=10)

    @staticmethod
    def get_user_transactions_for_symbol(user, symbol):
        def calculate_net_investment(trans_dict):
            total = 0
            buy_quantity = 0
            sell_quantity = 0
            try:
                position = RobinHoodPositions.objects.get(user=user, symbol=symbol)
                outstanding_position_quantity = position.quantity
            except RobinHoodPositions.DoesNotExist:
                outstanding_position_quantity = 0
            for instance in trans_dict['buy']:
                if outstanding_position_quantity:
                    outstanding_position_quantity -= instance.cumulative_quantity
                    if outstanding_position_quantity >= 0:
                        instance.cumulative_quantity = 0
                total -= (instance.average_price * instance.cumulative_quantity)
                buy_quantity += instance.cumulative_quantity
            for instance in trans_dict['sell']:
                total += (instance.average_price * instance.cumulative_quantity)
                sell_quantity += instance.cumulative_quantity

            if buy_quantity or sell_quantity:
                return {
                    'net': total,
                    'difference': buy_quantity - sell_quantity,
                    'symbol': symbol.symbol
                }
            return None

        if isinstance(symbol, basestring):
            symbol = Symbol.objects.get(symbol=symbol)

        transactions = RobinHoodTransaction.objects.filter(user=user,
                                                           symbol=symbol,
                                                           cumulative_quantity__gt=0).order_by('-id')
        transaction_dict = dict(buy=[], sell=[])
        for transaction_instance in transactions:
            transaction_dict[transaction_instance.side].append(transaction_instance)

        return calculate_net_investment(transaction_dict)

    @staticmethod
    def get_user_transactions(user):
        user_transaction_symbols = RobinHoodTransaction.objects.filter(user=user).values_list('symbol__symbol',
                                                                                              flat=True).distinct()
        results = {}
        for symbol in user_transaction_symbols:
            symbol_transaction = UserFinances.get_user_transactions_for_symbol(user, symbol)
            if symbol_transaction:
                results[symbol_transaction['symbol']] = symbol_transaction['net']
        return results

class UpdateSymbol(object):
    @staticmethod
    @transaction.atomic
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
        symbol_container = []
        current_symbols = set()
        for company in companies:
            symbol_ = company[0].strip()
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
            for title, url in [('Yahoo', 'https://finance.yahoo.com/quote/%s'),
                               ('StockTwits', 'https://stocktwits.com/symbol/%s')]:
                link, created = Link.objects.get_or_create(symbol_id=symbol.id, title=title)
                link.url = url % symbol.symbol
                link.link_type = 'generated'
                link.save()
                symbol.links.add(link)
            symbol_container.append(symbol)
            current_symbols.add(symbol_)

        batch_size = 10  # SQLite Limitation is low...
        bulk_update(symbol_container, batch_size=batch_size)

        symbol_container = []
        for symbol__ in all_symbols.difference(current_symbols):
            symbol = Symbol.objects.get(symbol=symbol__)
            symbol.listed = False
            symbol_container.append(symbol)
        batch_size = 10  # SQLite Limitation is low...
        bulk_update(symbol_container, batch_size=batch_size)

    @staticmethod
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
            historic_data, date_format = get_historic(symbol.symbol, now_minus_five_years)
            if historic_data:
                SymbolHistory.objects.filter(symbol=symbol).delete()

            symbol_history_list = []
            for day in historic_data:
                symbol_history_list.append(SymbolHistory(
                    symbol=symbol,
                    date=datetime.datetime.strptime(day[0], date_format),
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
        except AssertionError as e:
            print "%s:%s" % (symbol.symbol, str(e))
        return symbol

    @staticmethod
    @transaction.atomic
    def get_yahoo_symbol_news(symbol):
        response = get_stock_news(symbol.symbol)
        if isinstance(response, dict):
            if response.get('Content'):
                results = response['Content'].get('result')
                for result in results:
                    url = result.get('url')
                    if url:
                        symbol_news, created = SymbolNews.objects.get_or_create(symbol_id=symbol.id, url=url)
                        symbol_news.author = result.get('author_name')
                        symbol_news.title = result.get('title')
                        symbol_news.publisher = result.get('provider_name')
                        symbol_news.publisher_time = result.get('provider_publish_time')
                        symbol_news.summary = result.get('summary')
                        symbol_news.tag = result.get('tag')
                        symbol_news.timezone = result.get('timeZoneFullName')
                        # todo - Add a parsing lib to find the article div based on domain instead of including adds/banners/nav/etc
                        req = requests.get(url, verify=False)
                        if req.status_code == 200:
                            afinn = Afinn()
                            symbol_news.sentiment_analysis = afinn.score(req.content)
                        symbol_news.save()
                        symbol.news.add(symbol_news)
        symbol.save()

    @staticmethod
    @transaction.atomic
    def get_symbol_profile(symbol):
        response = get_stock_statistics(symbol.symbol)
        if isinstance(response, dict):
            if response.get('quoteSummary'):
                result = response['quoteSummary'].get('result')
                if result:
                    result = result[0]
                    asset_profile = result.get('assetProfile')
                    balance_sheet_profile = result.get('balanceSheetHistory')
                    balance_sheet_history_quarterly = result.get('balanceSheetHistoryQuarterly')
                    calendar_events = result.get('calendarEvents')
                    cashflow_statement_history = result.get('cashflowStatementHistory')
                    default_key_statistics = result.get('defaultKeyStatistics')
                    earnings = result.get('earnings')
                    financial_data = result.get('financialData')
                    fund_ownership = result.get('fundOwnership')
                    income_statement_history = result.get('incomeStatementHistory')
                    income_statement_history_quarterly = result.get('incomeStatementHistoryQuarterly')
                    inside_holders = result.get('insiderHolders')
                    insider_transactions = result.get('insiderTransactions')
                    institution_ownership = result.get('institutionOwnership')
                    major_direct_holders = result.get('majorDirectHolders')
                    major_holder_breakdown = result.get('majorHoldersBreakdown')
                    net_share_purchase_activity = result.get('netSharePurchaseActivity')
                    recommendation_trend = result.get('recommendationTrend')
                    security_filings = result.get('secFilings')
                    summary_profile = result.get('summaryProfile')
                    upgrade_downgrade_history = result.get('upgradeDowngradeHistory')

                    symbol_profile, created = SymbolProfile.objects.get_or_create(symbol_id=symbol.id)

                    symbol_profile.address = summary_profile.get('address1')
                    symbol_profile.city = summary_profile.get('city')
                    symbol_profile.state = summary_profile.get('state')
                    symbol_profile.country = summary_profile.get('country')
                    symbol_profile.zipcode = summary_profile.get('zip')
                    symbol_profile.phone = summary_profile.get('phone')
                    symbol_profile.website = summary_profile.get('website')
                    symbol_profile.summary = summary_profile.get('longBusinessSummary')
                    symbol_profile.number_of_employees = summary_profile.get('fullTimeEmployees')
                    for officer in asset_profile.get('companyOfficers'):
                        symbol_officer, created = SymbolOfficers.objects.get_or_create(symbol_id=symbol.id,
                                                                                       name=officer.get('name'))
                        symbol_officer.age = officer.get('age')
                        symbol_officer.title = officer.get('title')
                        total_pay = officer.get('totalPay', {})
                        symbol_officer.salary = total_pay.get('raw')
                        exercised_value = officer.get('exercisedValue', {})
                        symbol_officer.exercised_value = exercised_value.get('raw')
                        unexercised_value = officer.get('unexercisedValue', {})
                        symbol_officer.unexercised_value = unexercised_value.get('raw')
                        symbol_officer.save()
                        symbol_profile.officers.add(symbol_officer)

                    symbol_profile.save()
                    symbol.profile = symbol_profile
                    symbol.save()


class SymbolCalculations(object):
    @staticmethod
    @transaction.atomic
    def get_average_percent_change(symbol, day_count=100):
        historic_days = list(SymbolHistory.objects.filter(symbol=symbol).order_by('date'))[-day_count:]
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


if __name__ == '__main__':
    from app.tasks import refresh_daily_stats

    symbol = Symbol.objects.get(symbol='NUGT')
    user = User.objects.first()
    # print RobinHoodTransaction.objects.all().count()
    # UserFinances.retrieve_user_transactions_from_rh(user)
    pprint.pprint(sorted(UserFinances.get_user_transactions(user).items(), key=operator.itemgetter(1), reverse=True) )
    # print UserFinances.get_user_transactions_for_symbol(user, symbol)
    # print UserFinances.retrieve_user_positions(user)
    # print UserFinances.get_user_positions_for_symbol(user, symbol)

