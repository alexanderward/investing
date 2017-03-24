import datetime
from celery.schedules import crontab
from celery.task import periodic_task

from celery.utils.log import get_task_logger

from app.task_functions import get_user_financials, get_user_positions, get_listed_stocks, get_symbol_history, \
    get_average_percent_change

from app.models import User, Symbol
from bulk_update.helper import bulk_update

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour='8-17', day_of_week="mon-fri")))  # , minute="*/5")))
def update_robinhood_users_information():
    logger.info("Starting: Getting RobinHood User Information Task")
    for user in User.objects.all():
        get_user_financials(user)
        get_user_positions(user)
    logger.info("Finished: Getting RobinHood User Information Task")


@periodic_task(run_every=(crontab(hour='1', day_of_week="mon-fri")))
def refresh_daily_stats():
    logger.info("Starting: Getting all listed stocks for NASDAQ")
    get_listed_stocks()
    logger.info("Finished: Getting all listed stocks for NASDAQ")
    symbols = Symbol.objects.filter(listed=True)
    update_symbols = list()
    for symbol in symbols:
        logger.info("Starting: Getting all listed stocks historical stocks")
        symbol = get_symbol_history(symbol)
        logger.info("Completed: Getting all listed stocks historical stocks")
        symbol = get_average_percent_change(symbol, day_count=100)
        update_symbols.append(symbol)
    batch_size = 10  # SQLite Limitation is low...
    bulk_update(update_symbols, batch_size=batch_size)
