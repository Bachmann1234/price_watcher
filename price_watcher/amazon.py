import requests
from bs4 import BeautifulSoup

_OFFER_URL = "https://www.amazon.com/gp/offer-listing/{product_id}/?ie=UTF8"


def _format_price(price):
    return float(price.strip().replace(",", "").replace("$", ""))


def get_url(product_id):
    return _OFFER_URL.format(product_id=product_id)


def get_current_prices(product_id):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
    }
    response = requests.get(get_url(product_id), headers=headers)
    response.raise_for_status()
    simplified_response = "\n".join(
        line for line in response.text.split("\n") if line.strip().startswith("<")
    )
    soup = BeautifulSoup(simplified_response, "html.parser")
    return [
        _format_price(price.text)
        for price in soup.find_all("span", {"class": "olpOfferPrice"})
        if price
    ]
