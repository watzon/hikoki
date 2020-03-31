#!/usr/bin/env python3

# This file helps you create a session file for your bot.
# This must be run before attempting to run your bot.
# Please fill out the .env file with the requisite
# information as well.

from os import environ as env
from telethon import TelegramClient
from telethon.sessions import StringSession

try:
    from dotenv import load_dotenv
    load_dotenv()
except BaseException:
    pass

API_ID = env.get("API_ID", None)
API_HASH = env.get("API_HASH", None)

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Here's your session key. Place this in your .env file as " \
        "SESSION or expose a SESSION environment variable in another way.")
    print(client.session.save())
