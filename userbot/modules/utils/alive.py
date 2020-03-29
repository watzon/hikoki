from platform import python_version
from telethon import version as telethon_version

from userbot import bot, is_mongo_alive
from userbot.modules import ALL_MODULES
from userbot.commands import Command, register

@register
class AliveCommand(Command):
    """Use to check if your bot is alive and see some
    basic information."""

    command = "alive"
    category = "utils"

    async def exec(self, event):
        username = (await bot.get_me()).username

        if is_mongo_alive():
            database_status = "running"
        else:
            database_status = "failing :("

        message = f"**Hello, {username}. Your bot is running!**\n" \
                f"Telethon version: {telethon_version.__version__}\n" \
                f"Python version: {python_version()}\n" \
                f"Database status: {database_status}\n" \
                f"Modules loaded: {len(ALL_MODULES)}"

        await event.message.respond(message, parse_mode="markdown")


