# Price Watcher
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://travis-ci.org/Bachmann1234/price_watcher.svg?branch=master)](https://travis-ci.org/Bachmann1234/price_watcher)
[![codecov](https://codecov.io/gh/Bachmann1234/price_watcher/branch/master/graph/badge.svg)](https://codecov.io/gh/Bachmann1234/price_watcher)

This repo is a script I wrote to help watch a product page 
on amazon. Basically waiting to see if the product drops below a certain price.

The following will check the page and text the number 2025550112 if it finds a price < $1000

```bash
price_watcher B01FV4TAKK 1000 2025550112
```

the intended use of this script is as something you would throw into a cron task (or an aws lambda function like I did)
and let it watch a page for you

## Developing

Simply setup a virtualenv and install the requirements and install the source formatting githook

```bash
virtualenv -p python3 venv
pip install -r requirements.txt
pre-commit install
```

Running the tests
```bash
source venv/bin/activate
python -m pytest tests
```

Running the code formatter

```bash
source venv/bin/activate
black .
```

## Known Issues
I wrote this for one very specific product. 
It works for others (specifically ones that have a [Offer Listing](https://www.amazon.com/gp/offer-listing/B01FV4TAKK/ref=dp_olp_new_mbc?ie=UTF8&condition=new)) but I have not had a need yet so I have not seen how robust the scrape is.

I'm down for talking about improvements if people see this and are interested. But I mostly wrote this to watch this one product for my wife. It started as a simple script but then I was having fun writing it in a somewhat maintainable way
