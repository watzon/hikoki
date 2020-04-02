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
        await event.delete()

        dbchat = Chat.objects(chat_id=event.chat_id).get() # pylint: disable=no-member
        bancommand = dbchat.ban_command
        args, maybe_user = parse_arguments(event.pattern_match.group(1), [ 'user', 'reason' ])
        parts = re.split(r'\s+', maybe_user, 1)
        args['user'] = args.get('user') or parts[0]

        if len(parts) > 1 and not args.get('reason'):
            args['reason'] = parts[1]
        else:
            args['reason'] = ''

        reason = args.get('reason')

        try:
            user_full = await get_user_from_event(event, **args)
        except BaseException:
            user_full = None

        if not user_full:
            await log_message("**Failed to get information for user**\n" \
                              f"Command: `{event.message.message}`")
            return

        if event.reply_to_msg_id:
            reply = event.reply_to_msg_id
            await event.respond(f"{bancommand} {reason}", reply_to=reply)
        else:
            user_full = await get_user_from_event(event)
            await event.respond(f"{bancommand} {user_full.user.id} {reason}")
