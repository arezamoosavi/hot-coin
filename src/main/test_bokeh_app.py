import logging
import pandas as pd

from bokeh.plotting import figure, output_file, show, save
from bokeh.models import DatetimeTickFormatter
from twisted.internet import task, reactor

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)


# prepare some data
mydf = pd.read_csv(
    "mycsvfile.csv", names=["date", "amount"], parse_dates=["date"], header=None
)
y_value = mydf.iloc[:, 1]

# output to static HTML file
save_path = "test.html"
output_file(save_path)


TOOLS = "pan,wheel_zoom,box_zoom,reset,undo,save,hover"
p = figure(
    title="bitcoin value", x_axis_type="datetime", y_axis_label="usd", tools=TOOLS
)
p.sizing_mode = "stretch_width"

# add some renderers
p.line(mydf.index, y_value, legend_label="real ", line_color="blue")
# p.circle(range(1,arr1.shape[0]), arr1, legend_label="real power", line_color="blue", fill_color="blue")

p.line(
    mydf.index, y_value * 1.05, legend_label="stimated ", line_color="red",
)
# p.circle(range(1,arr1.shape[0]), arr2, legend_label="model power", line_color="red",  fill_color="red")


p.xaxis.formatter = DatetimeTickFormatter(
    hours=["%d %B %Y"], days=["%d %B %Y"], months=["%d %B %Y"], years=["%d %B %Y"],
)
# show the results
# show(p)
save(p)
