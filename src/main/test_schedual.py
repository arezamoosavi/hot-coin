import logging
import requests

import schedule
import time

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)


url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"


def job():
    resp = requests.get(url=url)
    data = resp.json()
    print(data)


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
