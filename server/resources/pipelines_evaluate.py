import tempfile
import json
from flask import request
from flask_restful import Resource
from boutiques.evaluate import evaluateEngine
from boutiques.localExec import LocalExecutor
from server.resources.decorators import login_required
from server.resources.helpers.pipelines import get_original_descriptor_path_and_type


class PipelinesEvaluate(Resource):
    # Generate a list of output file names given inputs
    @login_required
    def post(self, user, pipeline_identifier):
        (boutiques_descriptor_path, descriptor_type
         ), error = get_original_descriptor_path_and_type(pipeline_identifier)

        if error:
            return marshal(error), 400
        body = request.get_json(force=True)
        invocation = body['invocation']
        queries = body['queries']
        inv_tmp = tempfile.NamedTemporaryFile(mode="r+", delete=True)
        try:
            json.dump(invocation, inv_tmp)
            inv_tmp.flush()
            executor = LocalExecutor(boutiques_descriptor_path, inv_tmp.name, {
                "forcePathType": True,
                "destroyTempScripts": True,
                "changeUser": True
            })
            query_results = []
            for query in queries:
                query_results += [evaluateEngine(executor, query)]
            inv_tmp.close()
            return query_results[0] if len(query_results) == 1 else query_results, 200
        except Exception as error:
            inv_tmp.close()
            raise error
