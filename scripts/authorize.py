#!/usr/bin/env python3

# This file helps you create a session file for your bot.
# This must be run before attempting to run your bot.
# Please fill out the .env file with the requisite
# information as well.

from os import environ as env
import mongoengine
from telemongo import MongoSession
from telethon import TelegramClient
from telethon.sessions import StringSession

try:
    from dotenv import load_dotenv
    load_dotenv()
except BaseException:
    pass

API_ID = env.get("API_ID", None)
API_HASH = env.get("API_HASH", None)

MONGO_DB = env.get("MONGO_DB", "hikoki")
MONGO_USER = env.get("MONGO_USER", "hikoki")
MONGO_PASS = env.get("MONGO_PASS", "hikoki")
MONGO_HOST = env.get("MONGO_HOST", "127.0.0.1")
MONGO_PORT = env.get("MONGO_PORT", 27017)
MONGO_AUTH_DB = env.get("MONGO_AUTH_DB", None)

auth_source = f"?authSource={MONGO_AUTH_DB}" if MONGO_AUTH_DB else ""
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}{auth_source}"

# Set up the database
MONGO_CONNECTION = mongoengine.connect(MONGO_DB, host=MONGO_URI)

with TelegramClient(MongoSession(MONGO_DB, host=MONGO_URI), API_ID, API_HASH) as client:
    client.start()
