from userbot.db import Chat
from userbot.utils import get_user_from_event
from userbot.commands import Command, register

@register
class BanCommand(Command):
    """Ban a user in the current group using that group's
    specific ban command. The command can be set with
    `.config bancommand [command]`."""

    command = "ban"
    category = "admin"

    async def exec(self, event):
        chat = event.chat
        dbchat = Chat.objects(chat_id=chat.id).get() # pylint: disable=no-member
        bancommand = dbchat.ban_command

        if event.reply_to_msg_id:
            reply = event.reply_to_msg_id
            await event.respond(bancommand, reply_to=reply)
        else:
            maybe_user = event.pattern_match.groups()[0]
            user_full = await get_user_from_event(event, user=maybe_user)
            await event.respond(f"{bancommand} {user_full.user.id}")

        await event.delete()
