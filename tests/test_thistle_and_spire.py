import os
import responses

from price_watcher.thistle_and_spire import get_url, get_product_status


def _load_response_file(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


@responses.activate
def test_mocked_response():
    product_name = "medusa-bralette-chameleon"
    with open(_load_response_file("product_page_medusa-bralette-chameleon")) as infile:
        response = infile.read()
    responses.add(responses.GET, get_url(product_name), body=response, status=200)

    result = get_product_status(product_name)
    expected_result = {"L": True, "M": True, "S": True, "XL": False, "XS": True}
    assert result == expected_result
