from datetime import datetime

import click

from price_watcher.amazon import get_product_info, get_url
from price_watcher.notifications import send_text


def write_result(history_file, prices):
    with open(history_file, "a+") as outfile:
        outfile.write(
            "{}|{}\n".format(
                datetime.utcnow().isoformat(), ",".join(str(price) for price in prices)
            )
        )


@click.command()
@click.argument("product_id", type=click.STRING)
@click.argument("target_price", type=click.FLOAT)
@click.argument("phone_number", type=click.STRING)
@click.option(
    "--history_file", type=click.Path(dir_okay=False, writable=True), required=False
)
def check_product(product_id, target_price, phone_number, history_file):
    product_info = get_product_info(product_id)
    minimum_price = min(product_info.prices)
    print("Min: {}".format(minimum_price))
    print(product_info.prices)
    if history_file:
        write_result(history_file, product_info.prices)
    if minimum_price <= target_price:
        send_text(
            "Found {} for ${}! {}".format(
                product_info.name, minimum_price, get_url(product_id)
            ),
            phone_number,
        )
