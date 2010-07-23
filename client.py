#!/usr/bin/env python

from mendeley.mendeley_client import MendeleyClient
from creds import consumer_key, consumer_secret

mendeley = MendeleyClient(consumer_key, consumer_secret)
try:
    mendeley.load_keys()
except IOError:
    mendeley.get_required_keys()
    mendeley.save_keys()

