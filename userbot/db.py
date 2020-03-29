from mongoengine import Document, IntField, StringField, BooleanField

class Chat(Document):
    chat_id = IntField(primary_key=True, required=True) # pylint: disable=invalid-name
    title = StringField(required=True)
    kind = StringField()
    bot_disabled = BooleanField(default=False)

class GBanChat(Document):
    chat_id = IntField(primary_key=True, required=True)
    command = StringField(default="/gban")

class FBanChat(Document):
    chat_id = IntField(primary_key=True, required=True)
    command = StringField(default="/fban")
