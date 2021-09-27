# Self Test
import requests
from time import sleep

interval = 10
url = 'https://47b4-105-112-180-98.ngrok.io/ping'

# Ping dev server at intervals
while True:
    resp = requests.get(url)
    print(resp.text)
    sleep(interval)
