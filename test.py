# Self Test
import requests
from time import sleep

interval = 10
url = 'https://a10a-105-112-72-191.ngrok.io/ping'

# Ping dev server at intervals
while True:
    resp = requests.get(url)
    print(resp.text)
    sleep(interval)
