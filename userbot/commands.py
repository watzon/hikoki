import re
import sys
from abc import ABC, abstractmethod
import asyncio
import logging
import traceback
from time import gmtime, strftime

from telethon import TelegramClient
from telethon.events import NewMessage, MessageEdited
from telethon.tl.custom.message import Message

from userbot import bot, LOG_CHAT_ID, COMMAND_PREFIX
from userbot.models.chat import Chat

class Command(ABC):
    """This is the base `Command` class for other commands
    to inherit from."""

    #: The prefix to use for the command, defaults
    #: to the value of `COMMAND_PREFIX`.
    prefix: str = COMMAND_PREFIX

    #: The command itself, without the prefix.
    command: str = NotImplemented

    #: Aliases for the command. Order matters. When matched,
    #: these will be joined in a regular expression with
    #: `command` like `(?:command|alias1|alias2)`.
    aliases: [str] = None

    #: The category to add this command to. Defaults
    #: to 'uncategorized'.
    category: str = "uncategorized"

    #: If `True`, will not call this again if a
    #: message is edited.
    disable_edited: bool = False

    #: If `True`, this command will only work in groups.
    group_only: bool = False

    #: Disables error reporting for this command
    #: if something goes wrong.
    disable_errors: bool = False

    #: If `True`, this command will be usable by others,
    #: but not by you.
    incoming: bool = False

    #: If `True`, this command will still work in groups
    #: where the bot is disabled.
    disable_override: bool = False

    def __init__(self):
        # TODO: handle transforming pattern_match into arguments
        pass

    @abstractmethod
    async def exec(self, event: NewMessage):
        """This is the method that gets called when the command is matched."""

    @classmethod
    def on_register(cls, client: TelegramClient):
        """This gets called the first time the command is registered.
        Use it to do any setup."""

    @classmethod
    def help(cls):
        """Return the help text for this command."""
        help_text = re.sub(r"\s+", " ", cls.__doc__)
        usage = cls._build_usage()
        return f"**{cls.category}.{cls.command}**\n" \
               f"`{usage}`\n\n" \
               f"{help_text}"

    @classmethod
    def command_pattern(cls):
        """Returns the match pattern for this command."""
        aliases = cls.aliases or []
        aliases.insert(0, cls.command)
        command = '(?:' + '|'.join(aliases) + ')'
        pattern = '(?i)^' + re.escape(cls.prefix) + command + r'(\s+[\S\s]+)?$'
        return pattern

    @classmethod
    def subclasses(cls):
        """Gets all subclasses for this command."""
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in c.subclasses()])

    @classmethod
    def _build_usage(cls):
        return f"{COMMAND_PREFIX}{cls.command}"

def register(cls: Command.__class__):
    """Register a new `Command`"""
    pattern = cls.command_pattern()
    args = {'pattern': pattern, 'incoming': cls.incoming}

    async def decorator(check: Message):
        # pylint: disable=no-member
        db_chat = Chat.query.get(check.chat.id)
        if db_chat and not db_chat.bot_enabled and not cls.disable_override:
            return

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
        except BaseException as err:
            # Do some error handling. In the future we may make this more configurable,
            # but for now we just send a file to the log chat.

            # Log the error
            logging.error(err)

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
        bot.add_event_handler(decorator, MessageEdited(**args))
    bot.add_event_handler(decorator, NewMessage(**args))

    cls.on_register(bot)
    return decorator
