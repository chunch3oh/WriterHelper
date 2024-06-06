#!/bin/bash
rm -f book.db
python3 manage.py migrate
python3 manage.py runserver 7676

