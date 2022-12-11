''' sqlalcchemy module. '''
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String, Boolean
from . import Base as BaseDB


class TodoList(BaseDB):
    ''' creating todo list db '''
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True)
    task = Column(String(40))
    done = Column(Boolean, default=False)

    def __repr__(self):
        return f"TodoList(id={self.id!r}, task={self.task!r}, done={self.done!r})"
