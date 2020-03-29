from userbot import bot
from userbot.events import register

@register(outgoing=True, command="alive")
async def alive_command(e):
    username = (await bot.get_me()).username
    await e.reply("I seem to be running %s" % username)
