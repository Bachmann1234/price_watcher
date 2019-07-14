import requests
import attr
from bs4 import BeautifulSoup

_OFFER_URL = "https://www.amazon.com/gp/offer-listing/{product_id}/?ie=UTF8"


@attr.s
class ProductInfo(object):
    name = attr.ib()
    prices = attr.ib()


def _format_title(title):
    return title.strip().replace("Amazon.com: Buying Choices: ", "")


def _format_price(price):
    return float(price.strip().replace(",", "").replace("$", ""))


def _retrieve_product_page(product_id):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
    }
    response = requests.get(get_url(product_id), headers=headers)
    response.raise_for_status()
    return response


def _parse_page(product_page_response):
    simplified_response = "\n".join(
        line
        for line in product_page_response.text.split("\n")
        if line.strip().startswith("<")
    )
    return BeautifulSoup(simplified_response, "html.parser")


def get_url(product_id):
    return _OFFER_URL.format(product_id=product_id)


def get_product_info(product_id):
    product_offer_page = _parse_page(_retrieve_product_page(product_id))
    return ProductInfo(
        name=_format_title(product_offer_page.find("title").text),
        prices=[
            _format_price(price.text)
            for price in product_offer_page.find_all("span", {"class": "olpOfferPrice"})
            if price
        ],
    )
