#!/bin/sh

set -o errexit
set -o nounset


echo Wait
sleep 5000

exec "$@"