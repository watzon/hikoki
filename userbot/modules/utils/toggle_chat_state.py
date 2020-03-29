import logging

from userbot import LOG_CHAT_ID
from userbot.db import Chat
from userbot.commands import Command, register

@register
class DisableChatCommand(Command):
    """Disables the bot for the specified chat."""

    command = "disablechat"
    category = "utils"
    disable_override = True

    async def exec(self, event):
        chat_id = event.chat_id
        db_chat = Chat.objects(chat_id=chat_id).first() # pylint: disable=no-member

        if db_chat:
            db_chat.bot_disabled = True
            db_chat.save()
        else:
            logging.error("The chat with id `%d` doesn't seem to exist.", chat_id)

        await event.delete()
        await event.client.send_message(LOG_CHAT_ID, f"Bot disabled for chat `{chat_id}`")

@register
class EnableChatCommand(Command):
    """Enables the bot for the specified chat."""

    command = "enablechat"
    category = "utils"
    disable_override = True

    async def exec(self, event):
        chat_id = event.chat_id
        db_chat = Chat.objects(chat_id=chat_id).first() # pylint: disable=no-member

        if db_chat:
            db_chat.bot_disabled = False
            db_chat.save()
        else:
            logging.error("The chat with id `%d` doesn't seem to exist.", chat_id)

        await event.delete()
        await event.client.send_message(LOG_CHAT_ID, f"Bot enabled for chat `{chat_id}`")
