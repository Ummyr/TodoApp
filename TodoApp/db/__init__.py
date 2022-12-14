''' sqlalchemy ORM module. '''
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("sqlite:///TodoApp.sqlite", echo=True, future=True)
Base = declarative_base()

#pylint: disable-next=wrong-import-position; moving it up will result in circular import
from .todo import TodoList, Task

Base.metadata.create_all(engine)
session = Session(engine)
