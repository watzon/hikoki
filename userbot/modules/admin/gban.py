from userbot.db import Chat
from userbot.utils import get_user_from_event
from userbot.commands import Command, register

@register
class GBanCommand(Command):
    """Globally ban a user in each registered group using that
    group's gban command. The command can be set with
    `.config gbancommand [command]`."""

    command = "gban"
    category = "admin"

    async def exec(self, event):
        gban_chats = Chat.objects(gban_enabled=True) # pylint: disable=no-member
        reason = event.pattern_match.groups()[0] or ""

        for gbchat in gban_chats:
            bancommand = gbchat.gban_command
            user_full = await get_user_from_event(event)
            await event.client.send_message(gbchat.chat_id, f"{bancommand} {user_full.user.id} {reason}")

        await event.delete()
