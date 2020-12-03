import re
import difflib

from userbot.models.chat import Chat
# from userbot.utils import get_user_from_event
from userbot import COMMAND_PREFIX
from userbot.commands import Command, register

@register
class config(Command):
    """Check and set configuration options for the bot.
    Options if no option is provided, available options
    will be listed."""

    command = "config"
    category = "admin"

    async def exec(self, event):
        chat_id = event.chat.id
        params = event.pattern_match.groups()[0]
        options = ["fbans", "gbans", "bancommand", "gbancommand", "fbancommand"]
        if params:
            # We're either getting a value or setting one
            params = re.split(r'\s+', params.strip(), 1)
            option = params[0]
            newvalue = None
            if len(params) > 1:
                newvalue = params[1]

            if option == "bancommand":
                bcchat = Chat.query.get(chat_id)
                if newvalue:
                    bcchat.ban_command = newvalue
                    bcchat.commit()
                    await event.reply(f"Ban command for chat `{chat_id}` set to `{newvalue}`.")
                else:
                    ban_command = bcchat.ban_command
                    await event.reply(f"Ban command for chat `{chat_id}` is `{ban_command}`")
            elif option == "gbancommand":
                fbchat = Chat.query.get(chat_id)
                if newvalue:
                    fbchat.gban_command = newvalue
                    fbchat.commit()
                    await event.reply(f"Gban command for chat `{chat_id}` set to `{newvalue}`.")
                else:
                    gban_command = fbchat.gban_command
                    await event.reply(f"Gban command for chat `{chat_id}`: `{gban_command}`")
            elif option == "fbancommand":
                fbchat = Chat.query.get(chat_id)
                if newvalue:
                    fbchat.fban_command = newvalue
                    fbchat.commit()
                    await event.reply(f"Fban command for chat `{chat_id}` set to `{newvalue}`.")
                else:
                    fban_command = fbchat.fban_command
                    await event.reply(f"Fban command for chat `{chat_id}`: `{fban_command}`")
            elif option == "gbans":
                fbchat = Chat.query.get(chat_id)
                if newvalue:
                    boolean = self.str_to_bool(newvalue)
                    if boolean is None:
                        return await event.reply(f"Invalid value `{newvalue}` for option `gbans`.")
                    fbchat.gbans_enabled = boolean
                    fbchat.commit()
                    status = "enabled" if boolean else "disabled"
                    await event.reply(f"Gbans `{status}` for chat `{chat_id}`.")
                else:
                    status = "enabled" if fbchat.fbans_enabled else "disabled"
                    await event.reply(f"Gbans are `{status}` for chat `{chat_id}`.")
            elif option == "fbans":
                fbchat = Chat.query.get(chat_id)
                if newvalue:
                    boolean = self.str_to_bool(newvalue)
                    if boolean is None:
                        return await event.reply(f"Invalid value `{newvalue}` for option `fbans`.")
                    fbchat.fbans_enabled = boolean
                    fbchat.commit()
                    status = "enabled" if boolean else "disabled"
                    await event.reply(f"Fbans `{status}` for chat `{chat_id}`.")
                else:
                    status = "enabled" if fbchat.fbans_enabled else "disabled"
                    await event.reply(f"Fbans are `{status}` for chat `{chat_id}`.")
            elif option == "blacklist":
                echat = Chat.query.get(chat_id)
                if newvalue:
                    boolean = self.str_to_bool(newvalue)
                    if boolean is None:
                        return await event.reply(f"Invalid value `{newvalue}` for option `blacklist`.")
                    echat.bot_enabled = boolean
                    echat.commit()
                    status = "enabled" if boolean else "disabled"
                    await event.reply(f"Bot `{status}` for chat `{chat_id}`.")
                else:
                    status = "enabled" if echat.fbans_enabled else "disabled"
                    await event.reply(f"Bot is currenty `{status}` in chat `{chat_id}`.")
            else:
                close = difflib.get_close_matches(option, options)
                if len(close) > 0:
                    closest = close[0]
                    await event.reply(f"Unknown configuration option `{option}`.\n" \
                    f"Did you mean `{closest}`?")
                else:
                    await event.reply(f"Unknown configuration option `{option}`.")
        else:
            # Show a list of configuation options
            text =  "**Configuration**\n"
            text += "Here is a list of possible configuration options.\n"
            text += "To get an option's current value, use "
            text += f"`{COMMAND_PREFIX}config [option]`.\n"
            text += f"To set a value, use `{COMMAND_PREFIX}config [option] [new value]`.\n\n"
            for option in options:
                text += f"- `{option}`\n"

            await event.reply(text, parse_mode="markdown")

    def str_to_bool(self, string):
        if string.lower() in ["t", "true", "yes", "enable", "enabled"]:
            return True
        elif string.lower() in ["f", "false", "no", "disable", "enabled"]:
            return False
        return None
