from typing import Union

from telethon.tl.custom import Forward, Message
from telethon.tl.types import User, MessageEntityMention, MessageEntityMentionName
from telethon import TelegramClient

from userbot import spamwatch
from userbot.utils import helpers, constants, parse_arguments
from userbot.utils.mdtex import MDTeXDocument, Section, SubSection, KeyValueItem, Bold, Code, Link
from userbot.commands import Command, register


@register
class UserInfoCommand(Command):
    """Get information for the given user, either from a replied
    message, or a user id/username."""

    command = "user"
    aliases = ["u"]
    category = "utils"

    async def exec(self, event):
        msg: Message = event.message
        args, user = parse_arguments(event.pattern_match.group(1), ['id', 'all', 'general', 'bot', 'misc', 'search'])
        response = None

        if user:
            response = await self._info_from_user(event, **args)
        elif msg.is_reply:
            response = await self._info_from_reply(event, **args)

        if response:
            await event.respond(str(response))

    async def _info_from_user(self, event, **kwargs) -> MDTeXDocument:
        msg: Message = event.message
        client: TelegramClient = event.client
        keyword_args, args = await helpers.get_args(event)
        search_name = kwargs.get('search', False)
        if search_name:
            entities = [search_name]
        else:
            entities = [entity[1] for entity in msg.get_entities_text()
                        if isinstance(entity[0], (MessageEntityMention, MessageEntityMentionName))]

        # append any user ids to the list
        for uid in args:
            if isinstance(uid, int):
                entities.append(uid)

        users = []
        errors = []
        for entity in entities:
            try:
                user: User = await client.get_entity(entity)
                users.append(await self._collect_user_info(client, user, **keyword_args))
            except constants.GET_ENTITY_ERRORS:
                errors.append(str(entity))
        if users:
            return MDTeXDocument(*users,
                                 (Section(Bold('Errors for'),
                                          Code(', '.join(errors)))) if errors else '')

    async def _info_from_reply(self, event, **kwargs) -> MDTeXDocument:
        msg: Message = event.message
        client: TelegramClient = event.client
        get_forward = kwargs.get('forward', True)
        reply_msg: Message = await msg.get_reply_message()

        if get_forward and reply_msg.forward is not None:
            forward: Forward = reply_msg.forward
            user: User = await client.get_entity(forward.sender_id)
        else:
            user: User = await client.get_entity(reply_msg.sender_id)

        return MDTeXDocument(await self._collect_user_info(client, user, **kwargs))

    async def _collect_user_info(self, client, user, **kwargs) -> Union[Section, KeyValueItem]:
        id_only = kwargs.get('id', False)
        show_general = kwargs.get('general', True)
        show_bot = kwargs.get('bot', False)
        show_misc = kwargs.get('misc', False)
        show_all = kwargs.get('all', False)

        if show_all:
            show_general = True
            show_bot = True
            show_misc = True

        mention_name = kwargs.get('mention', False)

        full_name = await helpers.get_full_name(user)
        if mention_name:
            title = Link(full_name, f'tg://user?id={user.id}')
        else:
            title = Bold(full_name)

        if spamwatch:
            ban = spamwatch.get_ban(user.id)
            ban_reason = ban.reason if ban else None
        else:
            ban_reason = None

        if id_only:
            return KeyValueItem(title, Code(user.id))
        else:
            general = SubSection(
                Bold('general'),
                KeyValueItem('id', Code(user.id)),
                KeyValueItem('first_name', Code(user.first_name)),
                KeyValueItem('last_name', Code(user.last_name)),
                KeyValueItem('username', Code(user.username)),
                KeyValueItem('mutual_contact', Code(user.mutual_contact)),
                KeyValueItem('ban_reason', Code(ban_reason)) if ban_reason else KeyValueItem('gbanned', Code('False')))

            ibot = SubSection(
                Bold('bot'),
                KeyValueItem('bot', Code(user.bot)),
                KeyValueItem('bot_chat_history', Code(user.bot_chat_history)),
                KeyValueItem('bot_info_version', Code(user.bot_info_version)),
                KeyValueItem('bot_inline_geo', Code(user.bot_inline_geo)),
                KeyValueItem('bot_inline_placeholder',
                             Code(user.bot_inline_placeholder)),
                KeyValueItem('bot_nochats', Code(user.bot_nochats)))

            misc = SubSection(
                Bold('misc'),
                KeyValueItem('restricted', Code(user.restricted)),
                KeyValueItem('restriction_reason',
                             Code(user.restriction_reason)),
                KeyValueItem('deleted', Code(user.deleted)),
                KeyValueItem('verified', Code(user.verified)),
                KeyValueItem('min', Code(user.min)),
                KeyValueItem('lang_code', Code(user.lang_code)))

            return Section(title,
                           general if show_general else None,
                           misc if show_misc else None,
                           ibot if show_bot else None)
