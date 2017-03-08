import urllib

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
        req = requests.get(url)
        assert req.status_code == 200
        if req.headers.get('Content-Type') in ['text/csv', 'application/text', 'application/vnd.ms-excel']:
            return JankyCSV(req.content).get_rows(self.delimeter)
        return req.content


class Google(Source):
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
