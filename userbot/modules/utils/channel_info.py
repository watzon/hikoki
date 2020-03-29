from telethon import TelegramClient
from telethon.tl.types import Channel, User

from userbot.commands import Command, register
from userbot.utils.mdtex import MDTeXDocument, Section, KeyValueItem, Bold, Code

@register
class ChannelInfoCommand(Command):
    """Get informaton related to the given channel."""

    command = "chat"
    aliases = ["c"]
    category = "utils"

    async def exec(self, event):
        chat: Channel = await event.get_chat()
        client: TelegramClient = event.client
        if event.is_private:
            return
        chat_info = Section(Bold(f'Info for {chat.title}:'),
                            KeyValueItem(Bold('title'), Code(chat.title)),
                            KeyValueItem(Bold('chat_id'), Code(event.chat.id)),
                            KeyValueItem(Bold('access_hash'), Code(chat.access_hash)),
                            KeyValueItem(Bold('creator'), Code(chat.creator)),
                            KeyValueItem(Bold('broadcast'), Code(chat.broadcast)),
                            KeyValueItem(Bold('megagroup'), Code(chat.megagroup)),
                            KeyValueItem(Bold('min'), Code(chat.min)),
                            KeyValueItem(Bold('username'), Code(chat.username)),
                            KeyValueItem(Bold('verified'), Code(chat.verified)),
                            KeyValueItem(Bold('version'), Code(chat.version)))

        bot_accounts = 0
        total_users = 0
        deleted_accounts = 0
        user: User
        async for user in client.iter_participants(chat):
            total_users += 1
            if user.bot:
                bot_accounts += 1
            if user.deleted:
                deleted_accounts += 1

        user_stats = Section(Bold('user stats:'),
                            KeyValueItem(Bold('total_users'), Code(total_users)),
                            KeyValueItem(Bold('bots'), Code(bot_accounts)),
                            KeyValueItem(Bold('deleted_accounts'), Code(deleted_accounts)))

        # chat_document = client.db.groups.get_chat(event.chat_id)
        # db_named_tags: Dict = chat_document['named_tags'].getStore()
        # db_tags: List = chat_document['tags']
        # data = []
        # data += [KeyValueItem(Bold(key), value) for key, value in db_named_tags.items()]
        # data += [Item(_tag) for _tag in db_tags]
        # tags = Section('tags:', *data)
        info_msg = MDTeXDocument(chat_info, user_stats)
        await event.respond(str(info_msg))
