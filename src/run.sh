#!/bin/sh

set -o errexit
set -o nounset


echo Wait

python3 twisted_app.py & python3 bokeh_app.py

exec "$@"