import os

from twilio.rest import Client as TwilioClient

SID_ENV = "PRICE_WATCHER_SID"
AUTH_ENV = "PRICE_WATCHER_AUTH"
PHONE_NUM_ENV = "PRICE_WATCHER_PHONE_NUMBER"


def send_text(text, recipient_phone):
    # I am assuming a script that runs an exists in a cron job. If this becomes
    # Long living in some future this should be re thought
    print("Sending text to {}: '{}'".format(recipient_phone, text))
    TwilioClient(os.environ[SID_ENV], os.environ[AUTH_ENV]).messages.create(
        body=text, from_=os.environ[PHONE_NUM_ENV], to=recipient_phone
    )
