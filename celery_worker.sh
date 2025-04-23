#!/bin/sh
celery -A myproject worker --loglevel=info
