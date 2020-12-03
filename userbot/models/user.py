import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from userbot.db import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    is_bot = Column(Boolean, default=False)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    restricted = Column(Boolean, default=False)
    restriction_reason = Column(String)
    lang_code = Column(String)

    gbanned = Column(Boolean, default=False)
    gban_reason = Column(String)
    superuser = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


    def __repr__(self):
        return f"<User(id='{self.id}', first_name='{self.first_name}', last_name='{self.last_name}', username='{self.username}')>"

    def bot_api_id(self):
        return int(f"-100{self.id}")
