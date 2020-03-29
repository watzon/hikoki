from userbot.db import Chat
from userbot.utils import get_user_from_event
from userbot.commands import Command, register

@register
class FBanCommand(Command):
    """Fed ban a user in each registered fed using that
    fed's fban command. The command can be set with
    `.config fbancommand [command]`."""

    command = "fban"
    category = "admin"

    async def exec(self, event):
        fban_chats = Chat.objects(fban_enabled=True) # pylint: disable=no-member
        print(fban_chats.to_json())

        for fbchat in fban_chats:
            bancommand = fbchat.fban_command
            maybe_user = event.pattern_match.groups()[0]
            user_full = await get_user_from_event(event, user=maybe_user)
            await event.client.send_message(fbchat.chat_id, f"{bancommand} {user_full.user.id}")

        await event.delete()
