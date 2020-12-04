# This is the main entrypoint to your bot. Be sure to run
# scripts/authorize.py first to generate a session file.
import sys
import signal
import logging
from contextlib import suppress
from importlib import import_module

from telethon.tl.types import PeerUser
from telethon import events
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from userbot.models import User, Chat
# from userbot.commands import Command
from userbot import bot, LOG_CHAT_ID
from userbot.modules import ALL_MODULES
from userbot.messages import INVALID_PHONE, BOT_RESTARTED

def signal_handler(_sig, _frame):
    print('You pressed Ctrl+C! Exiting...')
    sys.exit(0)

async def cache_entities(update):
    user_id = None
    channel_id = getattr(update, 'channel_id', None)
    message = getattr(update, 'message', None)
    if not channel_id and message:
        if getattr(message, 'peer_id', None):
            if isinstance(message.peer_id, PeerUser):
                user_id = message.peer_id.user_id
            else:
                channel_id = message.peer_id.channel_id
        elif getattr(message, 'from_id', None):
            user_id = message.from_id.user_id

    if channel_id:
        with suppress(ValueError):
            channel = None
            with suppress(TypeError):
                channel = await bot.get_entity(channel_id)

            if channel:
                kind = "group"
                if channel.megagroup: kind = "megagroup"
                else: kind = "channel"

                record = Chat.query.get(channel_id)
                if record:
                    record.title = channel.title
                    record.kind = kind
                    record.is_admin = bool(channel.admin_rights)
                    record.commit()
                else:
                    record = Chat(id=channel_id, title=channel.title, kind=kind, is_admin=bool(channel.admin_rights))
                    record.save()

    if user_id:
        with suppress(ValueError):
            user = None
            with suppress(TypeError):
                user = await bot.get_entity(user_id)

            if user:
                record = User.query.get(user_id)
                if record:
                    record.first_name = user.first_name
                    record.last_name = user.last_name
                    record.username = user.username
                    record.restricted = user.restricted
                    record.restriction_reason = user.restriction_reason
                    record.lang_code = user.lang_code
                    record.commit()
                else:
                    record = User(id=user_id, first_name=user.first_name,
                        last_name=user.last_name, username=user.username,
                        restricted=user.restricted, restriction_reason=user.restriction_reason,
                        lang_code=user.lang_code)
                    record.save()

async def main():
    try:
        await bot.start()
    except PhoneNumberInvalidError:
        print(INVALID_PHONE)
        sys.exit(1)

    for module_name in ALL_MODULES:
        _ = import_module("userbot.modules." + module_name)

    logging.info("Your bot lives! You can validate this by running the .alive command.")

    # Keep track of chats
    bot.add_event_handler(cache_entities, events.Raw)

    # Tell the user the bot has been restarted
    if LOG_CHAT_ID:
        await bot.send_message(LOG_CHAT_ID, BOT_RESTARTED)

    # Set up our signal handler
    signal.signal(signal.SIGINT, signal_handler)

    await bot.run_until_disconnected()

if __name__ == "__main__":
    with bot:
        bot.loop.run_until_complete(main())
