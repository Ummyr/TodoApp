''' fask and flask restful module '''
from flask import Flask
from flask_restful import Api

from . import db, routes


app = Flask(__name__)
api = Api(app)
api.add_resource(routes.TodoTask, '/task/<int:task_id>', '/task')
api.add_resource(routes.TodoList, '/list/<int:todo_list_id>/<int:page>',
	'/list/<int:todo_list_id>', '/list')
