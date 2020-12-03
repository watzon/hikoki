import sys
import logging
from os import path, environ as env

import spamwatch
import sqlalchemy
import coloredlogs
from telethon import TelegramClient
from alchemysession import AlchemySessionContainer

# Setup environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except BaseException:
    pass

DB_URL = env.get("DB_URL", None)
API_ID = env.get("API_ID", None)
API_HASH = env.get("API_HASH", None)
LOG_CHAT_ID = int(env.get("LOG_CHAT_ID")) if env.get("LOG_CHAT_ID") else None
LOG_LEVEL = env.get("LOG_LEVEL", "DEBUG")
LOG_FILE = env.get("LOG_PATH", "bot.log")
LOG_FORMAT = env.get("LOG_FORMAT", "%(asctime)s %(name)s %(levelname)s %(message)s")
COMMAND_PREFIX = env.get("COMMAND_PREFIX", ".")
SPAMWATCH_HOST = env.get("SPAMWATCH_HOST", None)
SPAMWATCH_API_KEY = env.get("SPAMWATCH_API_KEY", None)

# Set up logging
_log_level = logging._nameToLevel[LOG_LEVEL] # pylint: disable=protected-access
_log_console_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(filename=LOG_FILE, filemode="w", level=_log_level)
logging.getLogger().addHandler(_log_console_handler)
coloredlogs.install(fmt=LOG_FORMAT, level=_log_level)

# Set up SpamWatch
if SPAMWATCH_API_KEY:
    spamwatch = spamwatch.Client(SPAMWATCH_API_KEY, host=SPAMWATCH_HOST)
else:
    spamwatch = None

alchemy_engine = sqlalchemy.create_engine(DB_URL, echo=False)

# Set up redis
# TODO

# Create the bot
container = AlchemySessionContainer(engine=alchemy_engine)
session = container.new_session('hikoki')
bot = TelegramClient(session, API_ID, API_HASH)
