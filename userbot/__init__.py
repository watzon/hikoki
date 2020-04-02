import sys
import logging
from os import path, environ as env

import spamwatch
import mongoengine
import coloredlogs
from telethon import TelegramClient

from telemongo import MongoSession

# Setup environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except BaseException:
    pass

API_ID = env.get("API_ID", None)
API_HASH = env.get("API_HASH", None)
LOG_CHAT_ID = int(env.get("LOG_CHAT_ID")) if env.get("LOG_CHAT_ID") else None
LOG_LEVEL = env.get("LOG_LEVEL", "DEBUG")
LOG_FILE = env.get("LOG_PATH", "bot.log")
LOG_FORMAT = env.get("LOG_FORMAT", "%(asctime)s %(name)s %(levelname)s %(message)s")
COMMAND_PREFIX = env.get("COMMAND_PREFIX", ".")
SPAMWATCH_HOST = env.get("SPAMWATCH_HOST", None)
SPAMWATCH_API_KEY = env.get("SPAMWATCH_API_KEY", None)

MONGO_DB = env.get("MONGO_DB", "hikoki")
MONGO_USER = env.get("MONGO_USER", "hikoki")
MONGO_PASS = env.get("MONGO_PASS", "hikoki")
MONGO_HOST = env.get("MONGO_HOST", "127.0.0.1")
MONGO_PORT = env.get("MONGO_PORT", 27017)
MONGO_AUTH_DB = env.get("MONGO_AUTH_DB", None)

auth_source = f"?authSource={MONGO_AUTH_DB}" if MONGO_AUTH_DB else ""
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}{auth_source}"

# Set up logging
_log_level = logging._nameToLevel[LOG_LEVEL] # pylint: disable=protected-access
_log_console_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(filename=LOG_FILE, filemode="w", level=_log_level)
logging.getLogger().addHandler(_log_console_handler)
coloredlogs.install(fmt=LOG_FORMAT, level=_log_level)

# Set up the database
MONGO_CONNECTION = mongoengine.connect(MONGO_DB, host=MONGO_URI)

def is_mongo_alive():
    try:
        mongoengine.get_connection()
    except BaseException:
        return False
    return True

# Set up redis
# TODO

# Set up SpamWatch
if SPAMWATCH_API_KEY:
    spamwatch = spamwatch.Client(SPAMWATCH_API_KEY, host=SPAMWATCH_HOST)
else:
    spamwatch = None

# Create the bot
bot = TelegramClient(MongoSession(MONGO_DB, host=MONGO_URI), API_ID, API_HASH)
