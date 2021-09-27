# Self Test
import requests
from time import sleep

interval = 10
url = 'https://a10a-105-112-72-191.ngrok.io/ping'

# Ping dev server at intervals
while True:
    try:
        resp = requests.get(url,params={'message':'Hi there, Server!'})
        print(resp.text)
        sleep(interval)
    except:
        print('Restarting process after 10s')
        sleep(10)
