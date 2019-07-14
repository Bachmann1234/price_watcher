from price_watcher.amazon import get_current_prices


def main():
    prices = get_current_prices('B01FV4TAKK')
    print(prices)
    print("Min: {}".format(min(prices)))
