import sys
from abc import ABC, abstractmethod
import asyncio
import logging
import traceback
from time import gmtime, strftime

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from userbot import bot, LOG_CHAT_ID, COMMAND_PREFIX

class Command(ABC):
    """This is the base `Command` class for other commands
    to inherit from."""

    prefix: str = COMMAND_PREFIX

    command: str = NotImplemented

    category: str = NotImplemented

    disable_edited: bool = False

    group_only: bool = False

    disable_errors: bool = False

    incoming: bool = False

    def __init__(self):
        # TODO: handle transforming pattern_match into arguments
        pass

    @abstractmethod
    async def exec(self, event):
        pass

    async def on_register(self, client: TelegramClient):
        pass

    @classmethod
    def help(cls):
        help_text = cls.__doc__
        usage = cls._build_usage()
        return f"**{cls.category}.{cls.command}**\n\n" \
               f"Usage: `{usage}`\n\n" \
               f"{help_text}"

    @classmethod
    def subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in c.subclasses()])

    @classmethod
    def _build_usage(cls):
        return f"{COMMAND_PREFIX}{cls.command}"

def register(cls: Command.__class__):
    """Register a new `Command`"""
    command = '(?i)^' + cls.prefix + cls.command
    args = {'pattern': command, 'incoming': cls.incoming}

    async def decorator(check: Message):
        if cls.group_only and not check.is_group():
            logging.warning(
                "Attempted to call method marked as group_only"
                "in a non-group setting.")
            return
        if cls.incoming and not check.out:
            await cls().exec(check)
            return

        try:
            await cls().exec(check)
        except KeyboardInterrupt:
            pass
        except BaseException as ex:
            # Do some error handling. In the future we may make this more configurable,
            # but for now we just send a file to the log chat.

            # Log the error
            logging.error(ex)

            if not cls.disable_errors and LOG_CHAT_ID != "":
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                text = ""

                command = "git log --pretty=format:\"%an: %s\" -5"
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                gitlog = str(stdout.decode().strip()) \
                    + str(stderr.decode().strip())

                title = "**Sorry, your bot encountered an error**"

                text += f"{title}\n\n"
                text += "Disclaimer: This file may contain sensitive information.\n"
                text += "            Be careful sharing it.\n\n"
                text += "--------BEGIN ERROR LOG--------\n"
                text += "Date: %s\n" % (date)
                text += "Group ID: %s\n" % (str(check.chat_id))
                text += "Sender ID: %s\n" % (str(check.sender_id))
                text += "Event Trigger:\n"
                text += str(check.text) + "\n\n"
                text += "Traceback info:\n"
                text += str(traceback.format_exc()) + "\n\n"
                text += "Error text:"
                text += str(sys.exc_info()[1]) + "\n\n"
                text += "---------END ERROR LOG---------\n\n"
                text += "Last 5 commits:\n"
                text += gitlog

                err_file = open("error.log", "w+")
                err_file.write(text)
                err_file.close()

                await check.client.send_file(
                    LOG_CHAT_ID,
                    "error.log",
                    caption=title,
                    parse_mode="markdown"
                )
        else:
            pass

    if not cls.disable_edited:
        bot.add_event_handler(decorator, events.MessageEdited(**args))
    bot.add_event_handler(decorator, events.NewMessage(**args))
    return decorator
