import json

import requests

requests.packages.urllib3.disable_warnings()


class NotLoggedIn(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(NotLoggedIn, self).__init__(message)


class RobinHood(object):
    def build_url(self, name, check=True):
        base_url = 'https://api.robinhood.com/'
        if (not self.portfolio_link or self.positions_link) and check:
            self.build_account_links()
            self.rebuilt_links = True
        urls = {
            'login': 'api-token-auth/',
            'logout': 'api-token-logout/',
            'account': 'accounts/',
            'portfolio': self.portfolio_link,
            'positions': self.positions_link,
            'transactions': 'orders/'
        }
        uri = urls.get(name)
        assert uri
        if 'https' in uri:
            return uri
        return "%s%s" % (base_url, uri)

    def __init__(self):
        self.rebuilt_links = False
        self.portfolio_link = None
        self.positions_link = None
        self.api_token = None

        self.account_balance_data = dict(available_funds=None, funds_held_for_orders=None, value=None)
        self.positions = dict()
        self.transactions = dict()

    def GET(self, url, data=""):
        return requests.get(url, headers={'Authorization': self.api_token})

    def POST(self, url, data={}):
        assert isinstance(data, dict)
        return requests.post(url, headers={'Authorization': self.api_token, 'content-type': 'application/json'},
                             data=data)

    def login(self, username, password):
        url = self.build_url('login', check=False)
        req = requests.post(url, data=json.dumps({'username': username, 'password': password}),
                            headers={'content-type': 'application/json'})
        if req.status_code == 200:
            data = req.json()
            self.api_token = "Token %s" % data.get('token')
            print self.api_token
            return True
        return False

    def logout(self):
        url = self.build_url('logout')
        req = self.POST(url)
        if req.status_code == 200:
            return True
        return False

    def build_account_links(self):
        url = self.build_url('account', check=False)
        req = self.GET(url)
        if req.status_code == 200:
            data = req.json().get('results')[0]
            self.portfolio_link = data.get('portfolio')
            self.positions_link = data.get('positions')
            self.__set_account_balance(data)
        elif req.status_code == 401:
            raise NotLoggedIn(req.text)
        else:
            raise Exception(req.text)

    def __set_account_balance(self, data):
        self.account_balance_data['funds_held_for_orders'] = data.get('cash_held_for_orders')
        self.account_balance_data['available_funds'] = data.get('buying_power')

    def get_account_balance(self):
        rebuilt_links = self.rebuilt_links
        url = self.build_url('account')
        if rebuilt_links == self.rebuilt_links:
            req = self.GET(url)
            if req.status_code == 200:
                data = req.json().get('results')[0]
                self.__set_account_balance(data)
            elif req.status_code == 401:
                raise NotLoggedIn(req.text)
            else:
                raise Exception(req.text)

        url = self.build_url('portfolio')
        req = self.GET(url)
        if req.status_code == 200:
            data = req.json()
            self.account_balance_data['value'] = data.get('equity')  # maybe use extended_hours_equity after hours...
        elif req.status_code == 401:
            raise NotLoggedIn(req.text)
        else:
            raise Exception(req.text)

        return self.account_balance_data

    def get_positions(self, url=None):
        if not url:
            url = self.build_url('positions')
        req = self.GET(url)
        results = []
        if req.status_code == 200:
            data = req.json().get('results')
            results.extend(data)
            next_url = req.json().get('next')
            if next_url:
                next_results = self.get_positions(next_url)
                results.extend(next_results)
            return results
        elif req.status_code == 401:
            raise NotLoggedIn(req.text)
        else:
            raise Exception(req.text)

    def get_transactions(self, url=None):
        if not url:
            url = self.build_url('transactions')
        req = self.GET(url)
        results = {}
        if req.status_code == 200:
            data = req.json().get('results')
            for record in data:
                if record['instrument'] not in results:
                    results[record['instrument']] = []
                results[record['instrument']].append(record)
            next_url = req.json().get('next')
            if next_url:
                next_results = self.get_transactions(next_url)
                for instrument, value in next_results.iteritems():
                    if instrument not in results:
                        results[instrument] = value
                    else:
                        results[instrument].extend(value)
            return results
        elif req.status_code == 401:
            raise NotLoggedIn(req.text)
        else:
            raise Exception(req.text)

if __name__ == '__main__':
    rh = RobinHood()
    from creds import get_robinhood_creds

    username, password = get_robinhood_creds()
    assert rh.login(username, password)
    # rh.logout()
    import pprint

    rh.get_account_balance()
    # pprint.pprint(rh.get_positions())
