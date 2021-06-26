LunchPy
===========
[![Status](https://img.shields.io/badge/status-alpha-red)](https://img.shields.io/badge/status-alpha-red)
[![API Coverage](https://img.shields.io/badge/endpoints_covered-10/18-yellow)](https://img.shields.io/badge/endpoints_covered-10/18-yellow)

## About

LunchPy is a python wrapper for Lunch Money's API. It requires an API key, which can be generated from your 
Lunch Money account under Settings -> Developers -> Request new Access Token. Note that the API itself
is in beta. This package should be considered experimental and breaking changes may be pushed without notice. This 
package does not currently cover the full set of Lunch Money API endpoints.

[API Documentation](https://lunchmoney.dev/#getting-started)

This package is built for Python 3.9.

## Install

	pip install lunchpy

This package's only requirement is the requests package.

## Setting up the API Key

Initialize an environment variable LUNCH_MONEY_API_KEY equal to your API key.

## Usage
```python
from lunchpy import Eat
api_key = ''
api = Eat(api_key)

for category in api.categories():
    print(f"You're so organized, you have a {category} category.")

transactions = api.transactions(start='2020-01-01', end='2020-02-01')
print(transactions[6]['amount'])
```

## Contributors

* [Vyryn](https://github.com/vyryn)

## TODO
- Expand coverage one endpoint at a time.
    - POST /categories
    - POST /transactions
    - PUT /transactions/:transaction_id
    - POST /transactions/group
    - PUT /budgets
    - DELETE /budgets
    - PUT /assets/:id
    - PUT /crypto/manual/:id

- Add tests for implemented endpoints
    - GET /categories
    - GET /transactions
    - GET /transactions/:transaction_id
    - GET /tags
    - GET /recurring_expenses
    - GET /budgets
    - GET /assets
    - GET /plaid_accounts
    - GET /crypto
    - DELETE transactions/group/:transaction_id