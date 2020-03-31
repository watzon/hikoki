import sys
import logging
from os import path, environ as env

import spamwatch
import mongoengine
import coloredlogs
from telethon import TelegramClient
from telethon.sessions import StringSession


# Setup environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except BaseException:
    pass

SESSION = path.join(env.get("SESSION", None))
API_ID = env.get("API_ID", None)
API_HASH = env.get("API_HASH", None)
LOG_CHAT_ID = int(env.get("LOG_CHAT_ID")) if env.get("LOG_CHAT_ID") else None
LOG_LEVEL = env.get("LOG_LEVEL", "DEBUG")
LOG_FILE = env.get("LOG_PATH", "bot.log")
LOG_FORMAT = env.get("LOG_FORMAT", "%(asctime)s %(name)s %(levelname)s %(message)s")
COMMAND_PREFIX = env.get("COMMAND_PREFIX", ".")
MONGO_DB_URI = env.get("MONGO_DB_URI", None)
MONGO_DB_NAME = env.get("MONGO_DB_NAME", "userbot")
SPAMWATCH_HOST = env.get("SPAMWATCH_HOST", None)
SPAMWATCH_API_KEY = env.get("SPAMWATCH_API_KEY", None)

# Set up logging
_log_level = logging._nameToLevel[LOG_LEVEL] # pylint: disable=protected-access
_log_console_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(filename=LOG_FILE, filemode="w", level=_log_level)
logging.getLogger().addHandler(_log_console_handler)
coloredlogs.install(fmt=LOG_FORMAT, level=_log_level)

# Set up the database
MONGO_CONNECTION = mongoengine.connect(MONGO_DB_NAME, host=MONGO_DB_URI)

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
bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
