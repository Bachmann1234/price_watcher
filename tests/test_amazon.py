import os
import responses

from price_watcher import get_current_prices
from price_watcher.amazon import get_url as amazon_product_url


def _load_response_file(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def test_live():
    result = get_current_prices("B01FV4TAKK")
    assert result
    assert len(result["prices"])
    assert result["title"]


@responses.activate
def test_mocked_response():
    product_id = "B01FV4TAKK"
    with open(_load_response_file("product_page_B01FV4TAKK.html")) as infile:
        response = infile.read()
    responses.add(
        responses.GET, amazon_product_url(product_id), body=response, status=200
    )

    result = get_current_prices(product_id)
    expected_result = {
        "title": "Tormek Sharpening System Magnum Bundle TBM803 T-8. A Complete Water Cooled Sharpener With 13 Popular Jigs and Accessories",
        "prices": [1235.0, 1235.0, 1235.0, 1235.99, 1438.6, 2090.64],
    }
    assert result == expected_result
