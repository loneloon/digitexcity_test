#!/bin/bash

echo "Django reset sequence initiated..."
echo ""
python3 manage.py wipe
echo ""
python3 manage.py makemigrations
echo""
python3 manage.py migrate
echo ""
python3 manage.py app_scrape
echo ""
echo "Reset sequence finished!"
