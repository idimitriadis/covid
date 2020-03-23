#!/bin/sh

cron
python get_data.py
python flask_app.py
