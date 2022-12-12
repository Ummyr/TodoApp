''' sqlalcchemy module. '''
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String, Boolean
from . import Base as BaseDB
from ..security import encrypt_data


class TodoList(BaseDB):
    ''' creating todo list db '''
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True)
    task = Column(String(40))
    done = Column(Boolean, default=False)

    def __repr__(self):
        return f"TodoList(id={self.id!r}, task={self.task!r}, done={self.done!r})"

    def to_dict(self):
        ''' converts row into dict that can be used for conversion into json '''
        return {
            'id': self.id,
            'task': self.task,
            'done': self.done
        }

    def to_dict_encrypted(self):
        ''' converts row into dict who's values are encrypted '''
        return {
            'id': encrypt_data(self.id),
            'task': encrypt_data(self.task),
            'done': encrypt_data(self.done)
        }
