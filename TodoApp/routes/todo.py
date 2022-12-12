''' importing flask resful module '''
from flask_restful import abort, Resource, reqparse

from ..db import TodoList as TodoListDB, session
from ..security import auth


def task_doesnt_exist(task_id):
    ''' generates a abort message on not finding task '''
    abort(404, message=f"Task {task_id} doesn't exist.")


class TodoTask(Resource):
    ''' to handle a single task from todo.'''
    @auth.login_required
    def get(self, task_id):
        ''' returns the task if it exists using id'''
        if task := session.query(TodoListDB).filter(TodoListDB.id==task_id).first():
            return task.to_dict_encrypted()
        task_doesnt_exist(task_id)
        return None

    @auth.login_required
    def post(self):
        '''adds a task to do'''
        parser = reqparse.RequestParser()
        parser.add_argument("task", required=True)
        args = parser.parse_args()

        with session:
            stmt = TodoListDB(
                task=args['task'],
            )
            session.add_all([stmt,])
            session.commit()

        return {'message':'sucessfully added new entry'}

    @auth.login_required
    def delete(self, task_id):
        ''' deletes a task using id'''
        query = session.query(TodoListDB).filter(TodoListDB.id==task_id)
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

        query = session.query(TodoListDB).filter(TodoListDB.id==task_id)

        if not query.first():
            task_doesnt_exist(task_id)
        if args['task'] is not None:
            query.update({'task': args['task']}, synchronize_session=False)
        if args['done'] is not None:
            query.update({'done': args['done']}, synchronize_session=False)

        session.commit()
        task = session.query(TodoListDB).filter(TodoListDB.id==task_id).first()
        return {'message':'sucessfully updated', 'data':task.to_dict_encrypted()}


class TodoList(Resource):
    ''' paginate a list of tasks in the todo '''

    @auth.login_required
    def get(self, page=0):
        ''' returns list of task to display on a page '''

        #search for query paramenter count
        parser = reqparse.RequestParser()
        parser.add_argument("count", type=int)
        args = parser.parse_args()

        count = 10
        if args['count']:
            count = args['count']

        query = session.query(TodoListDB).limit(count).offset(page*count)
        return [t.to_dict_encrypted() for t in query]
