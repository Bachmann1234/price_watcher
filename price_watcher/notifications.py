import os

from twilio.rest import Client as TwilioClient


def send_text(text, recipient_phone):
    # I am assuming a script that runs an exists in a cron job. If this becomes
    # Long living in some future this should be re thought
    TwilioClient(
        os.environ["PRICE_WATCHER_SID"], os.environ["PRICE_WATCHER_AUTH"]
    ).messages.create(
        body=text,
        from_=os.environ["PRICE_WATCHER_PHONE_NUMBER"],
        to=recipient_phone,
    )
