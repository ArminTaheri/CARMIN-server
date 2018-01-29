from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from server.config import Config

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

# from server.database.models.user import User
# db.create_all()
# db.session.commit()

from server.resources.authenticate import Authenticate
from server.resources.executions import Executions
from server.resources.execution import Execution
from server.resources.execution_kill import ExecutionKill
from server.resources.execution_play import ExecutionPlay
from server.resources.execution_stderr import ExecutionStdErr
from server.resources.execution_stdout import ExecutionStdOut
from server.resources.execution_results import ExecutionResults
from server.resources.executions_count import ExecutionsCount
from server.resources.path import Path
from server.resources.pipeline import Pipeline
from server.resources.pipelines import Pipelines
from server.resources.platform import Platform

api.add_resource(Platform, '/platform')
api.add_resource(Authenticate, '/authenticate')
api.add_resource(Executions, '/executions')
api.add_resource(ExecutionsCount, '/executions/count')
api.add_resource(Execution, '/executions/<string:execution_identifier>')
api.add_resource(ExecutionResults,
                 '/executions/<string:execution_identifier>/results')
api.add_resource(ExecutionStdOut,
                 '/executions/<string:execution_identifier>/stdout')
api.add_resource(ExecutionStdErr,
                 '/executions/<string:execution_identifier>/stderr')
api.add_resource(ExecutionPlay,
                 '/executions/<string:execution_identifier>/play')
api.add_resource(ExecutionKill,
                 '/executions/<string:execution_identifier>/kill')
api.add_resource(Pipelines, '/pipelines')
api.add_resource(Pipeline, '/pipelines/<string:pipeline_identifier>')
api.add_resource(Path, '/path/<string:complete_path>')


def main():
    """ Launch server"""
    app.run(host='0.0.0.0', port=int(8080))
