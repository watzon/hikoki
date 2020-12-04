import re

from userbot import spamwatch
from userbot.models.chat import Chat
from userbot.utils import get_user_from_event, log_message, parse_arguments
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
        await event.delete()
        fban_chats = Chat.query.filter(Chat.fbans_enabled == True).all()

        args, maybe_user = parse_arguments(event.pattern_match.group(1), [ 'user', 'reason' ])
        parts = re.split(r'\s+', maybe_user, 1)
        args['user'] = args.get('user') or parts[0]

        if len(parts) > 1 and not args.get('reason'):
            args['reason'] = parts[1]
        else:
            args['reason'] = 'spam [fban]'

        reason = args.get('reason')

        try:
            user_full = await get_user_from_event(event, **args)
        except BaseException:
            await log_message("**Failed to get information for user**\n" \
                              f"Command: `{event.message.message}`")

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
            await event.client.send_message(fbchat.id, f"{bancommand} {user_full.user.id} {reason}")

        await log_message(f"User `{user_full.user.id}` banned in {len(fban_chats)} chats.")
