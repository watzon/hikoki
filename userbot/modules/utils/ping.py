from datetime import datetime

from userbot.commands import Command, register

@register
class PingCommand(Command):
    """See how long it takes for a request to hit the server."""

    command = "ping"
    category = "utils"

    async def exec(self, event):
        start = datetime.now()
        await event.edit("`Pong!`")
        end = datetime.now()
        duration = (end - start).microseconds / 1000
        await event.edit("`Pong!\n%sms`" % duration)
