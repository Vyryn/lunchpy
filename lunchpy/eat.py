import datetime
import os

from collections import UserDict
from typing import Union

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
        name = self.get('name', None) or \
               self.get('original_name', None) or \
               self.get('category_name', None) or \
               super().__repr__()
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
        try:
            return [LunchPyResultObject(i) for i in res]
        except ValueError:
            raise RequestError(str(res)) from None

    def _query(self, endpoint: str, method: str = 'GET', extra_headers: dict = None, params: dict = None)\
            -> Union[dict, int]:
        """Internal helper function for building a query.
        Args:
            endpoint (str): Endpoint to query
            extra_headers (dict): Dictionary of extra headers to apply to this query
            params (dict): Dictionary of request parameters
        Returns:
            data (dict): Request data
        Raises:
            RequestError: Either the endpoint does not exist or LunchMoney responded with an error.
        """
        headers = dict(self.headers)
        if extra_headers:
            headers |= extra_headers
        resp = requests.request(method=method, url=self.endpoint + endpoint, headers=headers, params=params)
        data = resp.json()
        try:
            if data.get('error', None):
                raise RequestError(data['error'])
        except AttributeError:
            pass
        return data

    def categories(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to get a list of all categories associated with the user's account.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            categories ([LunchPyResultObject]): Requested categories
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query('categories', params=kwargs)
        return self._objectify(resp, 'categories')

    def transactions(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to retrieve all transactions between a date range.
        If no query parameters are set, this endpoint will return transactions for the
        current calendar month. Format for start and end are YYYY-MM-DD strings.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            transactions (list): list of Transaction dict/objects.
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query('transactions', params=kwargs)
        return self._objectify(resp, 'transactions')

    def transaction(self, tid: int, debit_as_negative: bool = False, **kwargs) -> LunchPyResultObject:
        """Use this endpoint to retrieve details about a specific transaction by ID.
        Args:
            tid (int): The transaction id you're looking for
            debit_as_negative (bool): Pass in true if you’d like expenses to be returned as negative
             amounts and credits as positive amounts. Defaults to false.
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            transaction (LunchPyResultObject): The requested transaction
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query(f'transactions/{tid}', params={'debit_as_negative': debit_as_negative} | kwargs)
        return LunchPyResultObject(resp)

    def tags(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to get a list of all tags associated with the user's account.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            tags ([LunchPyResultObject]): Requested tags
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.

        """
        resp = self._query('tags', params=kwargs)
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
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query('recurring_expenses', params=kwargs)
        return self._objectify(resp)

    def budgets(self, start_date: str = None, end_date: str = None, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to get full details on the budgets for all categories between a certain time period.
         The budgeted and spending amounts will be an aggregate across this time period.
        Args:
            start_date (str): The start date for this query in the form YYYY-MM-DD
            end_date (str): The end date for this query in the form YYYY-MM-DD
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            budgets ([LunchPyResultObject]): Requested budgets
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        if not start_date:
            start_date = str(datetime.date.today()-datetime.timedelta(days=30))
        if not end_date:
            end_date = str(datetime.date.today())
        resp = self._query('budgets', params={'start_date': start_date, 'end_date': end_date} | kwargs)
        return self._objectify(resp)

    def assets(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to get a list of all manually-managed assets associated with the user's account.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            assets ([LunchPyResultObject]): Requested assets
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query('assets', params=kwargs)
        return self._objectify(resp, 'assets')

    def plaid_accounts(self, **kwargs) -> [LunchPyResultObject]:
        """Use this endpoint to get a list of all synced Plaid accounts associated with the user's account.
        Plaid Accounts are individual bank accounts that you have linked to Lunch Money via Plaid. You may
        link one bank but one bank might contain 4 accounts. Each of these accounts is a Plaid Account.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            accounts ([LunchPyResultObject]): Requested accounts
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query('plaid_accounts', params=kwargs)
        return self._objectify(resp, 'plaid_accounts')

    def crypto(self, **kwargs) -> [LunchPyResultObject]:
        """
        Use this endpoint to get a list of all cryptocurrency assets associated with the user's account.
         Both crypto balances from synced and manual accounts will be returned.
        Args:
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            cryptos ([LunchPyResultObject]): Requested crypto assets
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        resp = self._query('crypto', params=kwargs)
        return self._objectify(resp, 'crypto')

    def del_group(self, tx_id: int) -> [int]:
        """Use this endpoint to delete a transaction group. The transactions within the group will not be removed.
        Args:
            tx_id (int): The transaction id of the group to remove
        Returns:
            removed ([int]): A list of the transaction ids of individual transactions that were removed
        """
        resp = self._query(f'transactions/group/{tx_id}', method='DELETE')
        try:
            return [int(i) for i in resp['transactions']]
        except KeyError:
            raise AttributeError(resp['error'])

    def del_budget(self, category_id: int, start_date: str = None) -> bool:
        """Use this endpoint to unset an existing budget for a particular category in a particular month.
        Args:
            start_date (str): The start date for the budget period in the form 'YYYY-MM'
            category_id (int): The uid for the category you're deleting the budget of
        Returns:
            success (bool): Whether the category was successfully deleted
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
            """
        params = {'start_date': f'{start_date}-01',
                  'category_id': str(category_id)}
        data = self._query('budgets', method='DELETE', params=params)
        return bool(data)

    def create_category(self, name: str, **kwargs):
        """Use this endpoint to create a single category.
        Args:
            name (str): Name of category. Must be 1-40 characters.
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            Result (int): The category id
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        data = self._query('categories', method='POST', params={'name': name} | kwargs)
        return int(data['category_id'])

    def create_transactions(self, transactions: [dict], **kwargs) -> [int]:
        """Use this endpoint to insert many transactions at once.
        Args:
            transactions ([dict]): List of transactions. Each transaction is a dict and must have date and amount
             parameters. Also accepts all optional parameters from the API.
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            Result ([int]): The category ids of successfully inserted transactions
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        data = self._query('transactions', method='POST', params={'transactions': transactions} | kwargs)
        return [int(i) for i in data['ids']]

    def create_transaction_group(self, date: str, payee: str, transactions: [int], **kwargs):
        """Use this endpoint to create a transaction group of two or more transactions.
        Returns the ID of the newly created transaction group
        Args:
            date (str): Date for the grouped transaction
            payee (str): Payee name for the grouped transaction
            transactions ([int]): List of two or more transaction ids to be part of the group
            kwargs (kwargs): A collection of key value pairs. Accepts all parameters the API does.
        Returns:
            Result (int): The id of the newly created transaction group
        Raises:
            RequestError: An error direct from Lunch Money. It will contain details.
        """
        params = {'date': date, 'payee': payee, 'transactions': transactions} | kwargs
        data = self._query('transactions/group', method='POST', params=params)
        return int(data)

    def update_transaction(self, transaction_id: int, **kwargs):
        """Use this endpoint to update a single transaction. You may also use this to split an existing transaction.
        Args:
            transaction_id (int): Updates to transaction matching ID

        :param transaction_id:
        :type transaction_id:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
