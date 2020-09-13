import logging
from datetime import datetime
import requests
import csv
import pandas as pd
from twisted.internet import task, reactor

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)


url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
timeout1 = 3.0
timeout2 = 5.0


def write_to_csv(amount, date):
    with open("mycsvfile.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount])

    with open("mycsvfile.csv") as f:
        print(f.read())


def doWork2():
    mydf = pd.read_csv(
        "mycsvfile.csv", names=["date", "amount"], parse_dates=["date"], header=None
    )
    print("Mydf:\n", mydf.tail())


def doWork1():
    resp = requests.get(url=url)
    data = resp.json()
    write_to_csv(data["data"]["amount"], datetime.utcnow())


l = task.LoopingCall(doWork1)
l.start(timeout1)

ll = task.LoopingCall(doWork2)
ll.start(timeout2)

reactor.run()
