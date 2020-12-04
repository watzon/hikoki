import random

from userbot.commands import Command, register

@register
class Copypasta(Command):
    """😩memify😩THe👐GIVen🚰🅱️ext😩"""

    EMOJIS = [
        "😂", "👌", "😂", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕",
        "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"
    ]

    command = "cp"
    category = "fun"

    async def exec(self, event):
        reply_message = await event.message.get_reply_message()
        message = reply_message if reply_message else event.message
        text = message.text

        reply = random.choice(self.EMOJIS)
        b_idx = random.randrange(0, len(text) - 1)

        for i, char in enumerate(text):
            if char == " ":
                reply += random.choice(self.EMOJIS)
            elif char in self.EMOJIS:
                reply += char
                reply += random.choice(self.EMOJIS)
            elif i == b_idx:
                reply += "🅱️"
            else:
                if random.choice([True, False]):
                    reply += char.upper()
                else:
                    reply += char.lower()

        reply += random.choice(self.EMOJIS)
        await event.edit(reply)
