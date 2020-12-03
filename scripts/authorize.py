#!/usr/bin/env python3

# This file helps you create a session file for your bot.
# This must be run before attempting to run your bot.
# Please fill out the .env file with the requisite
# information as well.

import os
import sqlalchemy
from alchemysession import AlchemySessionContainer
from telethon import TelegramClient

from dotenv import load_dotenv
load_dotenv()

DB_URL = os.environ.get("DB_URL", None)
API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)

alchemy_engine = sqlalchemy.create_engine(DB_URL)

container = AlchemySessionContainer(engine=alchemy_engine)
session = container.new_session('hikoki')
with TelegramClient(session, API_ID, API_HASH) as client:
    client.start()
