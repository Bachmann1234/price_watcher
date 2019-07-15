import click

from price_watcher.amazon import get_product_info, get_url
from price_watcher.notifications import send_text


@click.command()
@click.argument("product_id", type=click.STRING)
@click.argument("target_price", type=click.FLOAT)
@click.argument("phone_number", type=click.STRING)
def check_product_cli(product_id, target_price, phone_number):
    """
    Checks Amazon offers for the provided product id and texts the requested number
    if we find one below the provided target price

    This script depends on a working twilio client. To build one the script
    expects the following environment variables to be defined.
    Its the SID, the auth, and the phone number to use for sending texts.
    PRICE_WATCHER_SID
    PRICE_WATCHER_AUTH
    PRICE_WATCHER_PHONE_NUMBER
    """
    check_product(product_id, target_price, phone_number)


def check_product(product_id, target_price, phone_number):
    product_info = get_product_info(product_id)
    minimum_price = min(product_info.prices)
    print(product_info)
    if minimum_price <= target_price:
        send_text(
            "Found {} for ${}! {}".format(
                product_info.name, minimum_price, get_url(product_id)
            ),
            phone_number,
        )
