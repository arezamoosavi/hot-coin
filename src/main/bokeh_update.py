import logging
import pandas as pd
from datetime import datetime
import time
import requests

import csv
from tornado.ioloop import IOLoop
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.models.formatters import DatetimeTickFormatter


# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"


def write_to_csv(amount, date):
    with open("mycsvfile.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount])


def runner(doc):
    # initiate bokeh column data source
    test_data = ColumnDataSource({"Date": [], "Amount": []})

    # UPDATING FLIGHT DATA
    def update():
        # SEND REQUEST, READ RESPONSE AND LOAD AS JSON
        resp = requests.get(url=url)
        data = resp.json()
        write_to_csv(data["data"]["amount"], datetime.fromtimestamp(time.time()))

        # CONVERT TO PANDAS DATAFRAME
        mydf = pd.read_csv(
            "mycsvfile.csv", names=["Date", "Amount"], parse_dates=["Date"], header=None
        )
        # CONVERT TO BOKEH DATASOURCE AND STREAMING
        n_roll = len(mydf.index)
        test_data.stream(mydf.to_dict(orient="list"), n_roll)

    TOOLS = "pan,wheel_zoom,box_zoom,reset,undo,save,hover"
    p = figure(
        title="bitcoin value",
        x_axis_type="datetime",
        y_axis_label="USD",
        x_axis_label="Time",
        tools=TOOLS,
    )
    p.background_fill_color = "beige"
    p.background_fill_alpha = 0.5
    p.outline_line_width = 7
    p.outline_line_alpha = 0.3
    p.outline_line_color = "navy"

    p.sizing_mode = "stretch_both"
    p.line(
        source=test_data,
        x="Date",
        y="Amount",
        legend_label="real ",
        line_color="#f46d43",
        line_width=1,
        line_alpha=0.6,
    )
    p.circle(
        source=test_data,
        x="Date",
        y="Amount",
        legend_label="real",
        line_color="#3288bd",
        fill_color="white",
        line_width=5,
    )

    p.title.text_font_size = "20pt"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.xaxis.major_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "12pt"
    p.legend.label_text_font_size = "12pt"
    p.title.align = "center"
    p.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d %H:%M:%S")

    doc.add_periodic_callback(update, 3000)
    doc.add_root(p)


server = Server({"/": runner}, port=4000)
server.start()
IOLoop.current().start()
