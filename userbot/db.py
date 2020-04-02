from mongoengine import (Document, IntField, StringField, BooleanField,
                         ReferenceField, ListField, ImageField)

class Chat(Document):
    chat_id = IntField(primary_key=True, required=True) # pylint: disable=invalid-name
    title = StringField(required=True)
    kind = StringField()
    bot_disabled = BooleanField(default=False)

    ban_command = StringField(default="/ban")

    gban_enabled = BooleanField(default=False)
    gban_command = StringField(default="/ban")

    fban_enabled = BooleanField(default=False)
    fban_command = StringField(default="/fban")

class Note(Document):
    name = StringField(primary_key=True, required=True)
    chat = ReferenceField('Chat')
    content = StringField()
    tags = ListField()
    private = BooleanField(default=True)
    file = StringField()
