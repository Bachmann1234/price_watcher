# Price Watcher
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


This repo is a script I wrote to help watch a product page 
on amazon. Basically waiting to see if the product drops below a certain price.

The following will check the page and text the number 2025550112 if it finds a price < $1000

```bash
price_watcher B01FV4TAKK 1000 2025550112
```

This version does the same but appends the prices it finds to a history file

```bash
price_watcher B01FV4TAKK 1000 2025550112 --history_file=history.txt
```

the intended use of this script is as something you would throw into a cron task such that it runs periodically and texts
you if it finds an issue.

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
It works for others (specifically ones that have a [Offer Listing](https://www.amazon.com/gp/offer-listing/B01FV4TAKK/ref=dp_olp_new_mbc?ie=UTF8&condition=new)) but I have
not had a need yet so I have not seen how robust the scrape is

How do you best monitor a long running cron task? 
