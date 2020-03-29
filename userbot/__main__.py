# This is the main entrypoint to your bot. Be sure to run
# scripts/authorize.py first to generate a session file.
import sys
import signal
import logging
from importlib import import_module

from mongoengine import DoesNotExist

from telethon import events
from telethon.tl.types import InputPeerChannel, InputPeerChat, PeerChannel, PeerChat, UpdateNewMessage
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from userbot.db import Chat
from userbot.commands import Command
from userbot import bot, LOG_CHAT_ID
from userbot.modules import ALL_MODULES
from userbot.messages import INVALID_PHONE, BOT_RESTARTED

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Exiting...')
    sys.exit(0)

async def update_chat(update):
    if isinstance(update.to_id, PeerChannel):
        to_id = update.to_id.channel_id
        to_id = int(f"-100{to_id}")
    elif isinstance(update.to_id, PeerChat):
        to_id = update.to_id.chat_id
    else: return

    try:
        Chat.objects(chat_id=to_id).get()
    except DoesNotExist:
        input_entity = await bot.get_input_entity(to_id)

        if isinstance(input_entity, InputPeerChannel):
            ent = await bot(GetFullChannelRequest(input_entity.channel_id))
        elif isinstance(input_entity, InputPeerChat):
            ent = await bot(GetFullChatRequest(input_entity.chat_id))
        else: return

        for chat in ent.chats:
            try:
                id = int(f"-100{chat.id}")
                Chat(chat_id=id, title=chat.title).save()
                logging.debug("Saved new chat with id %d.", id)
            except BaseException:
                pass

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
    bot.add_event_handler(update_chat, events.NewMessage)

    # Tell the user the bot has been restarted
    if LOG_CHAT_ID:
        await bot.send_message(LOG_CHAT_ID, BOT_RESTARTED)

    # Set up our signal handler
    signal.signal(signal.SIGINT, signal_handler)

    await bot.run_until_disconnected()

if __name__ == "__main__":
    with bot:
        bot.loop.run_until_complete(main())
