#!/bin/bash
chmod -R +777 /app
chown 1200:1201 /app
python runserver.py
