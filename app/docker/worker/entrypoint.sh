#!/bin/bash
set -e

sleep 10

exec celery -A config worker -l INFO --concurrency=2
