"""
lunchpy API wrapper for the Lunch Money API
"""

__title__ = 'lunchpy'
__version__ = '0.0.1'
__author__ = 'Vyryn'
__license__ = 'GNU General Public License v3 (GPLv3)'

import requests


class RequestError(Exception):
    """Exception raised when an API request fails"""
    def __str__(self):
        return 'Failed to return the requested API.'


class Eat:
    """API Wrapper Class for Lunch Money"""

    def __init__(self, api_key: str, endpoint: str = "", version: str = 'v1'):
        """Creates a Eat object for querying the Lunch Money API.
        Args:
            endpoint (str, optional): Sets API endpoint. Defaults to the live Lunch Money endpoint.
        """
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = 'https://dev.lunchmoney.app/' + version + '/'

        self.headers = {'content-type': 'application/json',
                        'Authorization': 'Bearer ' + api_key}

    def _query(self, endpoint: str, extra_headers: dict = None, data: dict = None) -> dict:
        """Internal helper function for building a query.
        Args:
            endpoint (str): Endpoint to query
            extra_headers (dict): Dictionary of extra headers to apply to this query
            data (dict): Dictionary of Message Body Data
        Returns:
            data (dict): Request data
        Raises:
            RequestError: Likely, the requested API endpoint does not exist
        """
        headers = self.headers
        if extra_headers:
            headers |= extra_headers
        resp = requests.get(self.endpoint + endpoint, headers=headers, data=data)
        data = resp.json()
        if data.get('error', None):
            raise RequestError(data['error'])

        return data

    def categories(self) -> dict:
        """Use this endpoint to get a list of all categories associated with the user's account.
        Returns:
            categories (dict): Requested categories
        """
        resp = self._query('categories')
        res = {item['name']: item for item in resp['categories']}
        for item, properties in res:
            for key, value in properties:
                properties.__dict__[key] = value
        return res
