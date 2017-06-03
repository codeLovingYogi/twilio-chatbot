# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
import configparser
from twilio.rest import Client

CONFIG = configparser.ConfigParser()
CONFIG.read('keys.cfg')
ACCOUNT_SID = CONFIG['TWILIO']['ACCOUNT_SID']
AUTH_TOKEN = CONFIG['TWILIO']['AUTH_TOKEN']

ME = CONFIG['NUMBERS']['ME']
TWILIO = CONFIG['NUMBERS']['TWILIO']


client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.api.account.messages.create(to=ME,
                                             from_=TWILIO,
                                             body="Hi there!")