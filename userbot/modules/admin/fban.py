from userbot import spamwatch
from userbot.db import Chat
from userbot.utils import get_user_from_event
from userbot.commands import Command, register
from userbot.utils.constants import SPAMWATCH_CHAT_ID

@register
class FBanCommand(Command):
    """Fed ban a user in each registered fed using that
    fed's fban command. The command can be set with
    `.config fbancommand [command]`."""

    command = "fban"
    category = "admin"

    async def exec(self, event):
        fban_chats = Chat.objects(fban_enabled=True) # pylint: disable=no-member
        reason = event.pattern_match.groups()[0] or ""
        user_full = await get_user_from_event(event)

        await event.delete()

        if "spam" in reason:
            try:
                spamwatch.add_ban(user_full.user.id, reason)
            except BaseException:
                pass
            reply_message = await event.get_reply_message()
            if (event.chat_id != SPAMWATCH_CHAT_ID) and reply_message:
                await reply_message.forward_to(SPAMWATCH_CHAT_ID)

        for fbchat in fban_chats:
            bancommand = fbchat.fban_command
            await event.client.send_message(fbchat.chat_id, f"{bancommand} {user_full.user.id} {reason}")
