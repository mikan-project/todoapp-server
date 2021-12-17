from sqlalchemy import Column, Integer, String, Text

from db import Base


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    status = Column(Text)
