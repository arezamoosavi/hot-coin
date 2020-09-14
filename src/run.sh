#!/bin/sh

set -o errexit
set -o nounset


echo Wait

python twisted_app.py & python bokeh_app.py

exec "$@"