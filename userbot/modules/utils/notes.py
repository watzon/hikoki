import re
import difflib

from userbot.db import Note, Chat
from userbot.utils import log_message, parse_arguments
from userbot.commands import Command, register

@register
class NewNoteCommand(Command):
    """Adds a new note or overwrites an existing one."""

    command = "newnote"
    category = "utils"

    async def exec(self, event):
        await event.delete()
        args, note = parse_arguments(event.pattern_match.group(1), [ 'name', 'tags', 'local' ])
        reply_message = await event.get_reply_message()

        name = args.get('name')
        if not name:
            parts = re.split(r'\s+', note, 1)
            if len(parts) < 1:
                await log_message("Tried to create note with no name.")
                return
            name = parts[0]
            if len(parts) > 1:
                note = parts[1]

        tags = args.get('tags', [])
        if not isinstance(tags, list):
            tags = re.split(r',\s*', '')

        document = event.file
        if reply_message:
            if reply_message.message:
                note = reply_message.message
            document = reply_message.file

        chat = None
        if args.get('local'):
            chat = Chat.objects(chat_id=event.chat_id).get()

        note = Note(chat=chat,
                    name=name,
                    content=note,
                    tags=tags,
                    file=document.id if document else None)

        try:
            note.save()
            await log_message(f"**Note saved**\n  Name: `{name}`\n  Tags: `{', '.join(tags)}`")
        except BaseException as ex:
            print(ex)
            await log_message(f"Failed to save note with name `{name}`.")

@register
class NoteCommand(Command):
    """Fetches a note by name."""

    command = "note"
    category = "utils"

    async def exec(self, event):
        await event.delete()
        message = event.message.message
        parts = re.split('\s+', message)

        if len(parts) < 2:
            await log_message("Can't fetch a note with no name.")
            return

        name = parts[1]
        note = Note.objects(name=name).first()

        if not note:
            notes = (note.name for note in Note.objects)
            similar = difflib.get_close_matches(name, notes, 1)
            if len(similar) > 0:
                await log_message(f"No note named `{name}`. Did you mean `{similar[0]}`")
            else:
                await log_message(f"No note named `{name}`.")
            return

        if note.chat and note.chat.chat_id != event.chat_id:
            await log_message(f"Note `{name}` is local to chat `{note.chat}`.")
            return

        if note.file and note.file.strip() != '':
            await event.client.send_file(event.chat_id, note.file, caption=note.content)
        else:
            await event.respond(note.content)

@register
class NotesCommand(Command):
    """List all notes."""

    command = "notes"
    category = "utils"

    async def exec(self, event):
        # TODO: Filter by chat id
        tags = event.pattern_match.group(1) or ""
        tags = re.split(',\s*', tags.strip()) if tags.strip() != '' else []

        print(tags)

        if len(tags) > 0:
            notes = []
            for tag in tags:
                _notes = list(Note.objects(tags=tag))
                notes = notes + _notes
        else:
            notes = Note.objects

        print(notes)

        note_list = (note.name for note in notes)
        message = f"**Notes:**\n"
        for note in note_list:
            message += f"`{note}`\n"

        await event.respond(message)
