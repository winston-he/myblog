import json

WEBIM_REQUEST_HOST = 'https://a1.easemob.com'
ORG_NAME = '1110200924019019'
APP_KEY = '1110200924019019#demo'
APP_NAME = 'demo'
CLIENT_ID = 'YXA6HvC4NqgnR2uoCOf6l5cyOg'
CLIENT_SECRET = 'YXA6W1CQH4ZJ2rykvEp7iE9Q92I500E'

import redis

r = redis.StrictRedis(host="123.57.201.57", db=1, password="wins1603")
r.hset('webim_info', mapping={
    "org_name": '1110200924019019',
    "app_key": '1110200924019019#demo',
    "app_name": "demo",
    "client_id": "YXA6HvC4NqgnR2uoCOf6l5cyOg",
    "client_secret": "YXA6W1CQH4ZJ2rykvEp7iE9Q92I500E",
    "token": "",
    "host": 'https://a1.easemob.com'
})
