import logging

from userbot.utils import log_message
from userbot.commands import Command, register

@register
class CacheCommand(Command):
    """Iterate over the users in a group just to cache them."""

    command = "cache"
    category = "utils"

    async def exec(self, event):
        await event.delete()

        txt = f"**Caching users in chat `{event.chat.id}`**"
        message = await log_message(txt)

        total = 0
        async for user in event.client.iter_participants(event.chat.id, aggressive=True):
            total += 1
            if total % 100 == 0:
                await message.edit(txt + f"\nCached {total} so far")

            logging.debug("Caching user %d", user.id)

        await message.edit(txt + f"\nCached {total} users\nFinished")

