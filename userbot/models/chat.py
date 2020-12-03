import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from userbot.db import BaseModel

class Chat(BaseModel):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    kind = Column(String)

    bot_enabled = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    ban_command = Column(String, default="/ban")

    gbans_enabled = Column(Boolean, default=False)
    gban_command = Column(String, default="/ban")

    fbans_enabled = Column(Boolean, default=False)
    fban_command = Column(String, default="/fban")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Chat(id='{self.id}', title='{self.title}')>"

    def bot_api_id(self):
        return int(f"-100{self.id}")
