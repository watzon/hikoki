import difflib

from userbot.commands import Command, register


@register
class HelpCommand(Command):
    """Gets help for every registered command."""

    command = "help"
    category = "utils"

    async def exec(self, event):
        command_classes = Command.subclasses()

        # Build up a map of category -> command
        cat_map = {}
        cmd_map = {}
        for cls in command_classes:
            if not cls.category in cat_map:
                cat_map[cls.category] = []
            cat_map[cls.category].append(cls)
            cmd_map[cls.command] = cls.category

        matches = event.pattern_match.groups()
        if matches[0]:
            command = matches[0].strip()
            if command in cmd_map:
                cat_cmds = cat_map[cmd_map[command]]
                cmd = [cmd for cmd in cat_cmds if cmd.command == command][0]
                await event.respond(cmd.help(), parse_mode="markdown")
            else:
                close = difflib.get_close_matches(command, cmd_map.values())
                if len(close) > 0:
                    closest = close[0]
                    await event.respond(f"No match for command `{command}`.\n"
                                        f"Did you mean `{closest}`?")
                else:
                    await event.respond(f"No match for command `{command}`.")
        else:
            text = "**Please specify which module do you want help for**\n\n"
            for (key, cmds) in cat_map.items():
                command_names = sorted(cmd.command for cmd in cmds)
                text += f"**{key}**\n"
                text += ", ".join(f"`{cmd}`" for cmd in command_names)
                text += "\n\n"

            await event.respond(text, parse_mode="markdown")
