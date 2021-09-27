# Ahem...Testing, testing, 1, 2, 3
import requests
from time import sleep

# =========
# Test Me!
# =========

                                                            # ====================================
                                                            # Change message and push code to see 
                                                            # ping message updated on server end!
                                                            # ====================================

message = 'Hi there, Server!'                                                            
INTERVAL = 10
RESTART_AFTER = 10
DEV_SERVER_HOSTNAME = 'https://a10a-105-112-72-191.ngrok.io' # remember to update this. 

# Ping Development Server at intervals
while True:
    try:
        resp = requests.get(url=f'{DEV_SERVER_HOSTNAME}/ping',params={'message':f'{message}'})
        print(resp.text)
        sleep(INTERVAL)
    except:
        print(f'Restarting process after {RESTART_AFTER}s')
        sleep(RESTART_AFTER)
