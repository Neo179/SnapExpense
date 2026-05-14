#!/usr/bin/env bash

pip install -r requirements.txt
python configweb/manage.py collectstatic --noinput
python configweb/manage.py migrate