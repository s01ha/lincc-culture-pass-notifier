#!/bin/sh

/usr/local/bin/python3 /app/run.py --selenium-host=${SELENIUM_HOST} --selenium-port=${SELENIUM_PORT} --barcode=${BARCODE} --pin=${PIN} --bot-token=${BOT_TOKEN} --chat-id=${CHAT_ID}