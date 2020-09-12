import logging
import requests

from twisted.internet import task, reactor

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)


url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
timeout = 120.0


def doWork():
    resp = requests.get(url=url)
    data = resp.json()
    print(data)


l = task.LoopingCall(doWork)
l.start(timeout)

reactor.run()
