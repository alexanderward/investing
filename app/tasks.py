from celery.schedules import crontab
from celery.task import periodic_task

from celery.utils.log import get_task_logger
from datetime import datetime

from robinhood import RobinHood
from creds import get_robinhood_creds

from app.models import User, Financials

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour='8-17', day_of_week="mon-fri", minute="*/5")))
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
    Financials.objects.create(user=user,
                              available_funds=balance.get('available_funds'),
                              funds_held_for_orders=balance.get('funds_held_for_orders'),
                              portfolio_value=balance.get('value'))
    logger.info("Finished: Getting financials for %s" % email)


    # @periodic_task(run_every=(crontab(day_of_week="mon-fri")))  # every minute m-f
    # def get_user_positions():
    #     email = 'alexander.ward1@gmail.com'
    #     logger.info("Starting: Getting financials for %s" % email)
    #     user = User.objects.get(email=email)
    #     rh = RobinHood()
    #     if not user.rh_token:
    #         username, password = get_robinhood_creds()
    #         assert rh.login(username, password)
    #     else:
    #         rh.api_token = user.rh_token
    #     positions = rh.get_positions()
    #     # [{u'account': u'https://api.robinhood.com/accounts/5RY40845/',
    #     #   u'average_buy_price': u'56.5200',
    #     #   u'created_at': u'2017-02-17T18:33:02.718556Z',
    #     #   u'instrument': u'https://api.robinhood.com/instruments/09bc1a2d-534d-49d4-add7-e0eb3be8e640/',
    #     #   u'intraday_average_buy_price': u'0.0000',
    #     #   u'intraday_quantity': u'0.0000',
    #     #   u'quantity': u'2.0000',
    #     #   u'shares_held_for_buys': u'0.0000',
    #     #   u'shares_held_for_sells': u'2.0000',
    #     #   u'updated_at': u'2017-02-17T20:30:29.555872Z',
    #     #   u'url': u'https://api.robinhood.com/accounts/5RY40845/positions/09bc1a2d-534d-49d4-add7-e0eb3be8e640/'},
    #     # ]
    #     logger.info("Finished: Getting positions for %s" % email)
