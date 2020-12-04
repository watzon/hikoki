import re
from contextlib import suppress

from userbot import spamwatch
from userbot.models import Chat, User
from userbot.utils import get_user_from_event, parse_arguments, log_message
from userbot.utils.constants import SPAMWATCH_CHAT_ID
from userbot.commands import Command, register

@register
class GBanCommand(Command):
    """Globally ban a user in each registered group using that
    group's gban command. The command can be set with
    `.config gbancommand [command]`."""

    command = "gban"
    category = "admin"

    async def exec(self, event):
        await event.delete()
        gban_chats = Chat.query.filter(Chat.gbans_enabled == True).all()

        args, maybe_user = parse_arguments(event.pattern_match.group(1), [ 'user', 'reason' ])
        parts = re.split(r'\s+', maybe_user, 1)
        args['user'] = args.get('user') or parts[0]

        if len(parts) > 1 and not args.get('reason'):
            args['reason'] = parts[1]
        else:
            args['reason'] = 'spam [gban]'

        reason = args.get('reason')

        try:
            user_full = await get_user_from_event(event, **args)
        except BaseException:
            await log_message("**Failed to get information for user**\n" \
                              f"Command: `{event.message.message}`")
            return

        usermodel = User.query.get(user_full.id)
        if usermodel:
            usermodel.gbanned = True
            usermodel.gban_reason = reason
            usermodel.commit()

        if "spam" in reason:
            with suppress(BaseException):
                spamwatch.add_ban(user_full.user.id, reason)

            reply_message = await event.get_reply_message()
            if (event.chat_id != SPAMWATCH_CHAT_ID) and reply_message:
                await reply_message.forward_to(SPAMWATCH_CHAT_ID)

        for fbchat in gban_chats:
            bancommand = fbchat.gban_command
            await event.client.send_message(fbchat.id, f"{bancommand} {user_full.user.id} {reason}")

        await log_message(f"User `{user_full.user.id}` banned in {len(gban_chats)} chats.")
