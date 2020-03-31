import random

from userbot.commands import Command, register

@register
class MockCommand(Command):
    """Mocks the selected text like the [spongebob meme](https://knowyourmeme.com/memes/mocking-spongebob)."""

    command = "mock"
    category = "fun"

    async def exec(self, event):
        reply_text = list()
        textx = await event.get_reply_message()
        message = event.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await event.edit("gIvE sOMEtHInG tO MoCk!")
            return

        for charac in message:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)

        await event.edit("".join(reply_text))
