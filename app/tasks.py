import time
from celery.schedules import crontab
from celery.task import periodic_task

from celery.utils.log import get_task_logger

from app.models import User, Symbol
from bulk_update.helper import bulk_update

from app.task_functions import UserFinances, UpdateSymbol, SymbolCalculations
from app.utils import print_timer

logger = get_task_logger(__name__)
logger.setLevel(20)


@periodic_task(run_every=(crontab(hour='8-17', day_of_week="mon-fri")))  # , minute="*/5")))
def update_robinhood_users_information():
    logger.info("Starting: Getting RobinHood User Information Task")
    for user in User.objects.all():
        UserFinances.get_user_balance(user)
        UserFinances.get_user_positions(user)
    logger.info("Finished: Getting RobinHood User Information Task")


@periodic_task(run_every=(crontab(hour='1', day_of_week="mon-fri")))
def refresh_daily_stats():
    start = time.time()
    logger.info("Starting: Getting all listed stocks for NASDAQ")
    print("Starting: Getting all listed stocks for NASDAQ")
    UpdateSymbol.get_listed_stocks()
    end = time.time()
    logger.info("Finished: Getting all listed stocks for NASDAQ in: %s" % print_timer(start, end))
    print("Finished: Getting all listed stocks for NASDAQ in: %s" % print_timer(start, end))
    symbols = Symbol.objects.filter(listed=True)
    update_symbols = list()
    logger.info("Starting: Updating Stock History & Stats")
    print("Starting: Updating Stock History & Stats")
    start = time.time()
    for symbol in symbols:
        symbol = UpdateSymbol.get_symbol_history(symbol)
        symbol = SymbolCalculations.get_average_percent_change(symbol, day_count=20)
        update_symbols.append(symbol)
    batch_size = 10  # SQLite Limitation is low...
    bulk_update(update_symbols, batch_size=batch_size)
    end = time.time()
    logger.info("Finished: Updating Stock History & Stats in: %s" % print_timer(start, end))
    print("Finished: Updating Stock History & Stats in: %s" % print_timer(start, end))
    # Finished: Updating Stock History & Stats in: 00:38:39.42
