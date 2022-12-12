''' importing flask resful module '''
from flask_restful import abort, Resource, reqparse

from ..db import Task as TaskDB, session, TodoList as TodoListDB
from ..security import auth


def task_doesnt_exist(task_id):
    ''' generates a abort message on not finding task '''
    abort(404, message=f"Task {task_id} doesn't exist.")

def list_doesnt_exist(list_id):
    ''' generates a abort message on not finding list '''
    abort(404, message=f"To-Do List {list_id} doesn't exist.")


class TodoTask(Resource):
    ''' to handle a single task from todo.'''
    @auth.login_required
    def get(self, task_id):
        ''' returns the task if it exists using id'''
        if task := session.query(TaskDB).filter(TaskDB.id==task_id).first():
            return task.to_dict()
        task_doesnt_exist(task_id)
        return None

    @auth.login_required
    def post(self):
        '''adds a task to do'''
        parser = reqparse.RequestParser()
        parser.add_argument("task", required=True)
        parser.add_argument("todo_id", type=int, required=True)
        args = parser.parse_args()

        todo_list = session.query(TodoListDB).filter(TodoListDB.id==args['todo_id']).first()
        with session:
            stmt = TaskDB(
                task=args['task'],
            )
            todo_list.tasks.append(stmt)
            session.add_all([stmt,])
            session.commit()

        return {'message':'sucessfully added new entry'}

    @auth.login_required
    def delete(self, task_id):
        ''' deletes a task using id'''
        query = session.query(TaskDB).filter(TaskDB.id==task_id)
        if not query.first():
            task_doesnt_exist(task_id)

        query.delete(synchronize_session='fetch')
        session.commit()
        return {'message':'sucessfully deleted'}

    @auth.login_required
    def put(self, task_id):
        ''' updates the task using id'''
        parser = reqparse.RequestParser()
        parser.add_argument("task")
        parser.add_argument("done", type=bool)
        args = parser.parse_args()
        print(args)

        query = session.query(TaskDB).filter(TaskDB.id==task_id)

        if not query.first():
            task_doesnt_exist(task_id)
        if args['task'] is not None:
            query.update({'task': args['task']}, synchronize_session=False)
        if args['done'] is not None:
            query.update({'done': args['done']}, synchronize_session=False)

        session.commit()
        task = session.query(TaskDB).filter(TaskDB.id==task_id).first()
        return {'message':'sucessfully updated', 'data':task.to_dict()}


class TodoList(Resource):
    ''' paginate a list of tasks in the todo '''

    @auth.login_required
    def get(self, todo_list_id, page=0):
        ''' returns list of task to display on a page '''

        #search for query paramenter count
        parser = reqparse.RequestParser()
        parser.add_argument("count", type=int)
        args = parser.parse_args()

        count = 10
        if args['count']:
            count = args['count']

        query = (session.query(TaskDB).join(TodoListDB).filter(TodoListDB.id == todo_list_id)
            .limit(count).offset(page*count))
        return [t.to_dict() for t in query]

    @auth.login_required
    def post(self):
        '''create a to do list'''
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        args = parser.parse_args()

        with session:
            stmt = TodoListDB(
                title=args['title'],
            )
            session.add_all([stmt,])
            session.commit()

        return {'message':'sucessfully created new To-Do List'}

    @auth.login_required
    def delete(self, todo_list_id):
        ''' deletes entire todo list using id'''
        query = session.query(TodoListDB).filter(TodoListDB.id==todo_list_id)
        if not query.first():
            list_doesnt_exist(todo_list_id)

        query.delete(synchronize_session='fetch')
        session.commit()
        return {'message':'List sucessfully deleted'}
