#!/bin/sh
#Initialize DB
python create_schema.py

#Start gunicorn
exec gunicorn -w 4 -b 0.0.0.0:${PORT:-8089} wsgi:app
