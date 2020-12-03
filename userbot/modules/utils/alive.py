import os
import platform

import git
import telethon
import sqlalchemy
from platform import python_version

from userbot import bot
from userbot.utils.mdtex import MDTeXDocument, Section, KeyValueItem, Bold, Link
from userbot.modules import ALL_MODULES
from userbot.commands import Command, register

@register
class AliveCommand(Command):
    """Use to check if your bot is alive and see some
    basic information."""

    command = "alive"
    category = "utils"

    async def exec(self, event):
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        repo_url = os.environ.get("REPO_URL")
        repo_short = '/'.join(repo_url.split('/')[-2:])

        message = MDTeXDocument(
            Section(
                Bold("Hikōki"),
                KeyValueItem(Bold("version"), "0.2.0"),
                KeyValueItem(Bold("git hash"), sha[0:7]),
                KeyValueItem(Bold("repo url"), Link(repo_short, repo_url)),
                KeyValueItem(Bold("telethon version"), telethon.__version__),
                KeyValueItem(Bold("python version"), platform.python_version()),
                KeyValueItem(Bold("loaded modules"), len(ALL_MODULES))
            )
        )

        await event.message.respond(str(message), parse_mode="markdown", link_preview=False)


