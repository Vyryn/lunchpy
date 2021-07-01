LunchPy
===========
[![Status](https://img.shields.io/badge/status-beta-yellow)](https://img.shields.io/badge/status-beta-yellow)
[![API Coverage](https://img.shields.io/badge/endpoints_covered-18/18-g)](https://img.shields.io/badge/endpoints_covered-18/18-g)

## About

LunchPy is a python client for Lunch Money's API. It requires an API key, which can be generated from your 
Lunch Money account under Settings -> Developers -> Request new Access Token. Note that the API itself
is in beta. This package is also in beta; basic structure is complete but breaking changes may still be necessary.
This package covers the full set of 18 Lunch Money API endpoints as of 6/27/2021. Future endpoints and extensions 
should be supported automatically; _query can be used to query an endpoint directly, and additional parameters can 
freely be added to all calls without modification if they become supported by the API in the future.

[API Documentation](https://lunchmoney.dev/#getting-started)

This package is for Python 3.9 and uses [Semver 2.0.0](https://semver.org/spec/v2.0.0.html) versioning.

## Install

	pip install lunchpy

This package's only requirement is the requests package.

## Setting up the API Key

Initialize an environment variable LUNCH_MONEY_API_KEY equal to your API key. Alternatively, you can pass your API 
key to an Eat object on declaration. 

## Usage
```python
from lunchpy import Eat

api = Eat('your_api_key')

for category in api.categories():
    print(f'You have a category called {category}.')
```

## Contributors

* [Vyryn](https://github.com/vyryn)

## TODO

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
    - DELETE /budgets
    - POST /categories
    - POST /transactions
    - POST /transactions/group
    - PUT /transactions/:transaction_id
    - PUT /budgets
    - PUT /assets/:id
    - PUT /crypto/manual/:id