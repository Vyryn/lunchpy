LunchPy
===========
[![Status](https://img.shields.io/badge/-stable-brightgreen)](https://img.shields.io/badge/-stable-brightgreen)
[![API Coverage](https://img.shields.io/badge/endpoints_covered-18/18-g)](https://img.shields.io/badge/endpoints_covered-18/18-g)
[![Issues](https://img.shields.io/github/issues/Vyryn/lunchpy)](https://img.shields.io/github/issues/Vyryn/lunchpy)
[![License](https://img.shields.io/github/license/vyryn/lunchpy)](https://img.shields.io/github/license/vyryn/lunchpy)
## About

LunchPy is a python client for Lunch Money's API. It requires an API key, which can be generated from your 
Lunch Money account under Settings -> Developers -> Request new Access Token. Note that while this library is 
considered production-ready, the API itself is still in beta, so breaking changes may still come from the Lunch 
Money team.

This package covers the full set of 18 Lunch Money API endpoints as of 9/13/2021. Future endpoints and extensions 
as well as most breaking changes from the API itself should be supported by this library automatically; additional 
parameters can freely be added to all calls without modification if they become supported by the API in the future, 
and if all else fails _query can be used to query an endpoint directly.

[API Documentation](https://lunchmoney.dev/#getting-started)

This package is for Python 3.9 and uses [Semver 2.0.0](https://semver.org/spec/v2.0.0.html) versioning.

## Install

	pip install lunchpy

This package requires Requests version 25 or newer.

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

## Contributing

Contributions are welcome. With the 1.0.0 release this library is considered complete. If you would like to add 
additional functionality, the top 'nice to have' would be tests.
