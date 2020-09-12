import logging
import requests

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)


url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

resp = requests.get(url=url)
data = resp.json()

print("all: ", data)
print("data: ", data["data"])
print("amount: ", data["data"]["amount"])
