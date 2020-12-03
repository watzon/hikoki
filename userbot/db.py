from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from userbot import alchemy_engine

Session = scoped_session(sessionmaker(bind=alchemy_engine))
class _Base(object):
    query = Session.query_property()

    def save(self, commit=False):
        Session.add(self)
        if commit:
            Session.commit()

    def commit(self):
        Session.commit()

BaseModel = declarative_base(cls=_Base)

# class Note(Document):
#     name = StringField(primary_key=True, required=True)
#     chat = ReferenceField('Chat')
#     content = StringField()
#     tags = ListField()
#     private = BooleanField(default=True)
#     file = StringField()
