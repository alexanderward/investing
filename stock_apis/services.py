import re
import urllib

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from app.exceptions import StockDoesNotExist

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import datetime

# https://greenido.wordpress.com/2009/12/22/work-like-a-pro-with-yahoo-finance-hidden-api/
# https://www.quantshare.com/sa-43-10-ways-to-download-historical-stock-quotes-data-for-free
from stock_apis.data_wrangling import JankyCSV


class Source(object):
    def __init__(self):
        self.__url = None
        self.__parameters = {}
        self.__delimiter = ","

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url_):
        self.__url = url_
        self.__parameters = {}

    @property
    def delimeter(self):
        return self.__delimiter

    @delimeter.setter
    def delimeter(self, delimeter_):
        self.__delimiter = delimeter_

    @property
    def parameters(self):
        return urllib.urlencode(self.__parameters)

    def update_parameters(self, params):
        assert isinstance(params, dict)
        self.__parameters.update(params)

    def get_data(self):
        assert self.__url
        url = self.url
        if self.parameters:
            url = url + '?' + self.parameters
        print url
        req = requests.get(url)
        assert req.status_code == 200
        content_type = req.headers.get('Content-Type', "")
        if content_type in ['text/csv', 'application/text', 'application/vnd.ms-excel']:
            return JankyCSV(req.content).get_rows(self.delimeter)
        elif 'application/json' in content_type:
            return req.json()
        return req.content
        # else:
        #     raise StockDoesNotExist('\nStatus code: %s\n Content: %s' % (req.status_code, req.content))


class Google(Source):
    """
    Get's Historic data from Google
    """

    def __init__(self):
        super(Google, self).__init__()
        self.url = "https://www.google.com/finance/historical"
        self.delimeter = ','

    def get_symbol(self, symbol, from_date):
        now = datetime.datetime.now()
        self.update_parameters({'startdate': from_date.strftime('%b %d %Y'), 'enddate': now.strftime('%b %d %Y'),
                                'q': symbol, 'output': 'csv'})
        data = self.get_data()
        return data


class IChart(Source):
    def __init__(self):
        """
        Turns out that Yahoo has bugged results if the company is either not listed or something else happens.  Use
        Google class instead.
        """
        super(IChart, self).__init__()
        self.url = "http://ichart.yahoo.com/table.csv"
        self.delimeter = ','

    def get_symbol(self, symbol, from_date):
        now = datetime.datetime.now()
        self.update_parameters({'a': from_date.month - 1, 'b': from_date.day, 'c': from_date.year})  # From
        self.update_parameters({'d': now.month, 'e': now.day, 'f': now.year})  # To
        self.update_parameters({'s': symbol, 'g': 'd', 'ignore': '.csv'})
        data = self.get_data()
        return data


class NASDAQ(Source):
    """
    Gets a list of all stocks listed on the NASDAQ
    """

    def __init__(self):
        super(NASDAQ, self).__init__()
        self.url = "http://www.nasdaq.com/screening/companies-by-industry.aspx"
        self.delimeter = '",'

    def get_nasdaq_companies(self):
        self.update_parameters({'exchange': 'NASDAQ', 'render': 'download'})
        return self.get_data()

    def get_nyse_companies(self):
        self.update_parameters({'exchange': 'NYSE', 'render': 'download'})
        return self.get_data()


class YahooFinance(Source):
    """
    Get's the Stock's statistics from Yahoo
    https://finance.yahoo.com/quote/ATVI/key-statistics?p=ATVI <- Explained results for the most part
    """

    def __init__(self):
        super(YahooFinance, self).__init__()

    def get_statistics(self, symbol):
        url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/"
        self.url = "%s%s" % (url, symbol)
        self.update_parameters({
                                   'modules': 'defaultKeyStatistics,financialData,calendarEvents,assetProfile,'
                                              'secFilings,incomeStatementHistory,cashflowStatementHistory,'
                                              'balanceSheetHistory,incomeStatementHistoryQuarterly, '
                                              'cashflowStatementHistoryQuarterly,balanceSheetHistoryQuarterly,earnings,'
                                              'institutionOwnership,fundOwnership,majorDirectHolders,'
                                              'majorHoldersBreakdown,insiderTransactions,insiderHolders,'
                                              'netSharePurchaseActivity,summaryProfile,'
                                              'recommendationTrend,upgradeDowngradeHistory'})
        data = self.get_data()
        return data

    def get_news(self, symbol):
        self.url = "https://query2.finance.yahoo.com/v2/finance/news"
        self.update_parameters({'lang': 'en-US', 'region': 'US', 'symbols': symbol})
        data = self.get_data()
        return data

    def get_comments(self, symbol, context_ids=None):
        if not context_ids:
            self.url = "https://finance.yahoo.com/quote/%s/community?p=%s" % (symbol, symbol)
            data = self.get_data()
            context_ids = re.findall("messageBoardId\":\"(.*?)\"", data)
        results = []
        for context_id in context_ids:
            self.url = "https://finance.yahoo.com/_finance_doubledown/api/resource/canvass.getMessageListForContext_ns" \
                       ";context=%s;count=20;index=null;lang=en-US;namespace=yahoo_finance;oauthConsumerKey" \
                       "=finance.oauth.client.canvass.prod.consumerKey;oauthConsumerSecret=finance.oauth.client.canvass" \
                       ".prod.consumerSecret;region=US;sortBy=popular;type=null" % context_id
            data = self.get_data()
            results.append(data)
        return results

# print YahooFinance().get_comments('ATVI')
