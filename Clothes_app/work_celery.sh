#!/bin/sh
celery -A Clothes_app worker --beat -l INFO