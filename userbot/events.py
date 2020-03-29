import sys
import asyncio
import logging
import traceback
from time import gmtime, strftime

from telethon import events
from telethon.tl.custom.message import Message

from userbot import bot, LOG_CHAT_ID, COMMAND_PREFIX

def register(**args):
    """Register a new event"""
    pattern = args.get('pattern', None)
    command = args.get('command', None)
    command_prefix = args.get('prefix', COMMAND_PREFIX)
    # params = args.get('params', None)
    disable_edited = args.get('disable_edited', False)
    group_only = args.get('group_only', False)
    disable_errors = args.get('disable_errors', False)
    incoming_func = args.get('incoming', True)

    if not command and not pattern:
        logging.error("Either a command or a pattern is required")
        return

    if command and pattern:
        logging.error("Cannot have both a command and a pattern. Please choose one.")
        return

    if command:
        args['pattern'] = '(?i)^' + command_prefix + command
        # TODO: Handle params here

    if pattern and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    for arg in ["disable_edited", "group_only", "disable_errors", "command", "params"]:
        if arg in args:
            del args[arg]

    def decorator(func):
        async def wrapper(check: Message):
            if group_only and not check.is_group():
                logging.warning(
                    "Attempted to call method marked as group_only"
                    "in a non-group setting.")
                return
            if incoming_func and not check.out:
                await func(check)
                return

            try:
                await func(check)
            except KeyboardInterrupt:
                pass
            except BaseException:
                # Do some error handling. In the future we may make this more configurable,
                # but for now we just send a file to the log chat.

                if not disable_errors and LOG_CHAT_ID != "":
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

                    text += "**Sorry, your bot encountered an error**\n\n"
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
                        caption=text
                    )
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
