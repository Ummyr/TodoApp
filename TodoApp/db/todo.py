''' sqlalcchemy module. '''
from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship

from . import Base as BaseDB
from ..security import encrypt_data

#pylint: disable-next=too-few-public-methods; more methods are not needed
class TodoList(BaseDB):
    ''' creating todo list db '''
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True)
    title = Column(String(20))

    tasks = relationship(
         "Task", back_populates="todo_list", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"TodoList(id={self.id!r}, title={self.title!r})"


class Task(BaseDB):
    ''' creating todo tasks db '''
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String(40))
    done = Column(Boolean, default=False)
    todo_list_id = Column(Integer, ForeignKey("todo_list.id"), nullable=False)

    todo_list = relationship("TodoList", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id!r}, task={self.task!r}, done={self.done!r})"

    def to_dict(self):
        ''' converts row into dict that can be used for conversion into json '''
        return {
            'id': self.id,
            'task': self.task,
            'done': self.done,
            'todo_list_id': self.todo_list_id
        }

    def to_dict_encrypted(self):
        ''' converts row into dict who's values are encrypted '''
        return {
            'id': encrypt_data(self.id),
            'task': encrypt_data(self.task),
            'done': encrypt_data(self.done),
            'todo_list_id': encrypt_data(self.todo_list_id)
        }
