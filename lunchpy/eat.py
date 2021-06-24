import os

from collections import UserDict

import requests


class LunchPyResultObject(UserDict):
    """A dict-like object to enable reference by both attribute and as a dict."""

    def __getattr__(self, name):
        """Try returning an item with given `name` as a key."""
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(f'{self.__class__.__name__} object '
                                 f'has no attribute {name}') from None

    def __repr__(self):
        name = self.get('name', None) or self.get('original_name', None) or super().__repr__()
        return f'<{name}>'


class RequestError(Exception):
    """Exception raised when an API request fails"""

    def __init__(self, reason: str = None):
        self.reason = reason
        super().__init__(self)

    def __str__(self):
        if self.reason:
            return str(self.reason)
        return 'Failed to return the requested API.'


class NoEnvApiKeyError(Exception):
    def __str__(self):
        return "LunchPy requires an API key. Either initialize an Eat object with one or set the "\
               "'LUNCH_MONEY_API_KEY' environment variable."


class Eat:
    """API Wrapper Class for Lunch Money"""

    def __init__(self, api_key: str = '', endpoint: str = "", version: str = 'v1'):
        """Creates a Eat object for querying the Lunch Money API.
        Args:
            endpoint (str, optional): Sets API endpoint. Defaults to the live Lunch Money endpoint.
        """
        if endpoint:
            self.endpoint = endpoint.rstrip('/') + '/' + version.rstrip('/').lstrip('/') + '/'
        else:
            self.endpoint = 'https://dev.lunchmoney.app/' + version + '/'
        if api_key == '':
            api_key = os.getenv("LUNCH_MONEY_API_KEY")
            if not api_key:
                raise NoEnvApiKeyError from None
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'Bearer ' + api_key}

    @staticmethod
    def _objectify(res, ident=None) -> [LunchPyResultObject]:
        """Turn a list of dicts into a list of LunchPyResultObjects"""
        if ident:
            try:
                res = res[ident]
            except KeyError:
                raise RequestError(str(res))
        return [LunchPyResultObject(i) for i in res]

    def _query(self, endpoint: str, extra_headers: dict = None, params: dict = None) -> dict:
        """Internal helper function for building a query.
        Args:
            endpoint (str): Endpoint to query
            extra_headers (dict): Dictionary of extra headers to apply to this query
            params (dict): Dictionary of request parameters
        Returns:
            data (dict): Request data
        Raises:
            RequestError: Likely, the requested API endpoint does not exist
        """
        headers = dict(self.headers)
        if extra_headers:
            headers |= extra_headers
        resp = requests.get(self.endpoint + endpoint, headers=headers, params=params)
        data = resp.json()
        try:
            if data.get('error', None):
                raise RequestError(data['error'])
        except AttributeError:
            pass
        return data

    def categories(self) -> [LunchPyResultObject]:
        """Use this endpoint to get a list of all categories associated with the user's account.
        Returns:
            categories ([LunchPyResultObject]): Requested categories
        """
        resp = self._query('categories')
        return self._objectify(resp, 'categories')

    def transactions(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to retrieve all transactions between a date range.
        If no query parameters are set, this endpoint will return transactions for the
        current calendar month. Format for start and end are YYYY-MM-DD strings.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            transactions (list): list of Transaction dict/objects.
        """
        resp = self._query('transactions', params=kwargs)
        return self._objectify(resp, 'transactions')

    def transaction(self, tid: int, debit_as_negative: bool = False) -> LunchPyResultObject:
        """Use this endpoint to retrieve details about a specific transaction by ID.
        Args:
            tid (int): The transaction id you're looking for
            debit_as_negative (bool): Pass in true if you’d like expenses to be returned as negative
             amounts and credits as positive amounts. Defaults to false.
        Returns:
            transaction (LunchPyResultObject): The requested transaction
        """
        resp = self._query(f'transactions/{tid}', params={'debit_as_negative': debit_as_negative})
        return LunchPyResultObject(resp)

    def tags(self) -> [LunchPyResultObject]:
        """Use this endpoint to get a list of all tags associated with the user's account.
        Returns:
            tags ([LunchPyResultObject]): Requested tags
        """
        resp = self._query('tags')
        return self._objectify(resp)

    def recurring_expenses(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to retrieve a list of recurring expenses to expect for a specified period.
        Every month, a different set of recurring expenses is expected. This is because recurring expenses
        can be once a year, twice a year, every 4 months, etc. If a recurring expense is listed as “twice
        a month”, then that recurring expense will be returned twice, each with a different billing date
        based on when the system believes that recurring expense transaction is to be expected. If the
        recurring expense is listed as “once a week”, then that recurring expense will be returned
        in this list as many times as there are weeks for the specified month. In the same vein, if a
        recurring expense that began last month is set to “Every 3 months”, then that recurring expense
        will not show up in the results for this month.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            recurring ([LunchPyResultObject]): Requested recurring expenses
        """
        resp = self._query('recurring_expenses', params=kwargs)
        return self._objectify(resp)
