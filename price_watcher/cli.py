import click

from price_watcher.amazon import get_product_info, get_url
from price_watcher.notifications import send_text
from price_watcher.thistle_and_spire import get_product_status


@click.group()
def cli():
    pass


@cli.command()
@click.argument("product_id", type=click.STRING)
@click.argument("target_price", type=click.FLOAT)
@click.argument("phone_number", type=click.STRING)
def check_amazon_cli(product_id, target_price, phone_number):
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
    print(check_amazon_product(product_id, target_price, phone_number))


def check_amazon_product(product_id, target_price, phone_number):
    product_info = get_product_info(product_id)
    minimum_price = min(product_info.prices)
    if minimum_price <= target_price:
        send_text(
            "Found {} for ${}! {}".format(
                product_info.name, minimum_price, get_url(product_id)
            ),
            phone_number,
        )
    return product_info


@cli.command()
@click.argument("product_name", type=click.STRING)
@click.argument("size", type=click.STRING)
@click.argument("phone_number", type=click.STRING)
def check_thistle_and_spire_cli(product_name, size, phone_number):
    """
    For some reason on the site the sizes are called swatches
    I am guessing it used to be just color?
    """
    print(check_thistle_and_spire(product_name, size, phone_number))


def check_thistle_and_spire(product_name, size, phone_number):
    status_by_size = get_product_status(product_name)
    result = status_by_size.get(size.upper())
    msg = f"{product_name} in size {size} {'is' if result else 'is not'} in stock!"
    if result:
        send_text(msg, phone_number)
    return msg
