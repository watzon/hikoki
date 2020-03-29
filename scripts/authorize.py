#!/usr/bin/env python3

# This file helps you create a session file for your bot.
# This must be run before attempting to run your bot.
# Please fill out the .env file with the requisite
# information as well.

from os import path, environ as env
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = env.get("API_ID", None)
API_HASH = env.get("API_HASH", None)
SESSION = path.realpath(path.join(env.get("SESSION_DIR", "./"), "userbot"))

bot = TelegramClient(SESSION, API_ID, API_HASH)
bot.start()
