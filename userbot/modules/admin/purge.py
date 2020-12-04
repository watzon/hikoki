from userbot import bot
from userbot.commands import Command, register
from userbot.utils import parse_arguments

@register
class Purge(Command):
    """Purge all messages starting from the replied to message,
    or a number of messages going back in history."""

    command = "purge"
    category = "admin"

    async def exec(self, event):
        args, count = parse_arguments(event.pattern_match.group(1), [ 'silent', 'me' ])
        from_user = 'me' if args.get('me') else None

        reply_message = await event.message.get_reply_message()
        chat = await event.get_input_chat()
        messages = []

        # Delete the command message
        await event.delete()

        if reply_message:
            # If a message was replied to we'll delete all messages since that one
            async for msg in bot.iter_messages(chat, min_id=reply_message.id, from_user=from_user):
                messages.append(msg)
            messages.append(reply_message)
        else:
            # Otherwise we'll purge the last N messages, where N is `count`
            count = int(count)
            async for msg in bot.iter_messages(chat, from_user=from_user):
                if len(messages) >= count: break
                messages.append(msg)

        if len(messages) > 0:
            await bot.delete_messages(chat, messages)

        if not args.get('silent'):
            await event.respond(f"Purged {len(messages)} messages")
