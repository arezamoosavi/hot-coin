import os
from datetime import datetime
import requests
import csv
import pandas as pd
from joblib import dump, load
from twisted.internet import task, reactor
from sklearn.ensemble import RandomForestRegressor


url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"


DATA_INTERVAL_S = os.getenv("DATA_INTERVAL_S", 200)

ML_INTERVAL_S = os.getenv("ML_INTERVAL_S", 24 * 60 * 60)
# ML_INTERVAL_S = os.getenv("ML_INTERVAL_S", 20)

TRAIN_SAMPLE = int(10 * 60 * 60 / DATA_INTERVAL_S)
# TRAIN_SAMPLE = 100


def write_to_csv(amount, date):
    with open("bitcoin.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount])


def gather_data():
    try:
        resp = requests.get(url=url)
        data = resp.json()
        write_to_csv(data["data"]["amount"], datetime.utcnow())
    except:
        pass


def train_model():
    try:
        _df = pd.read_csv(
            "bitcoin.csv", names=["Date", "Amount"], parse_dates=["Date"], header=None
        )
        _df["Price_After_TenH"] = _df["Amount"].shift(-TRAIN_SAMPLE)
        _df.dropna(inplace=True)
        _df.drop(["Date"], axis=1, inplace=True)
        X = _df.drop(["Price_After_TenH"], axis=1)
        y = _df["Price_After_TenH"]
        reg = RandomForestRegressor(n_estimators=200, random_state=101)
        reg.fit(X, y)
        dump(reg, "bit_reg.joblib")
    except:
        pass


if __name__ == "__main__":
    try:
        l = task.LoopingCall(gather_data)
        l.start(DATA_INTERVAL_S)

        ll = task.LoopingCall(train_model)
        ll.start(ML_INTERVAL_S)

        reactor.run()
    finally:
        reactor.stop()
