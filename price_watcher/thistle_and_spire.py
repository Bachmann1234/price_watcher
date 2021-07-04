from typing import Dict

import requests
from bs4 import BeautifulSoup

_BASE_URL = "https://www.thistleandspire.com/products"


def get_url(name: str) -> str:
    return f"{_BASE_URL}/{name}"


def _retrieve_product_page(name: str) -> str:
    response = requests.get(get_url(name))
    response.raise_for_status()
    return response.text


def _parse_page(product_page_response):
    return BeautifulSoup(product_page_response, "html.parser")


def _find_size_swatch(parsed_result):
    for swatch in parsed_result.find_all("div", {"class": "swatch"}):
        if "Size" in str(swatch):
            return swatch


def get_product_status(name: str) -> Dict[str, bool]:
    result = _parse_page(_retrieve_product_page(name))
    swatch = _find_size_swatch(result)
    results = {}
    for element in swatch.find_all("div", {"class": "swatch-element"}):
        results[element.attrs["data-value"].upper()] = (
            "available" in element.attrs["class"]
        )
    return results
