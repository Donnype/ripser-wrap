"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""
import pandas as pd
import numpy as np
from flask import request, Response, json
from flask_restplus import Resource
from ripser import ripser

from .security import require_auth
from app.api import api_rest


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


def ndarray_to_object(data_array: np.ndarray, maxdim: int, prime: int, cocycles: bool):
    result = ripser(X=data_array, maxdim=maxdim, coeff=prime, do_cocycles=cocycles)
    diagrams = []
    cocycles = []

    for diagram in result['dgms']:
        if len(diagram) > 0 and diagram[-1][1] == np.Inf:
            diagram = diagram[:-1]

        diagrams.append(json.dumps(diagram.tolist()))

    for cocycles_in_dim in result['cocycles']:
        cc_in_dim = []

        for cocycle in cocycles_in_dim:
            cc_in_dim.append(cocycle.tolist())

        cocycles.append(json.dumps(cc_in_dim))

    return {
        'diagrams': json.dumps(diagrams),
        'cocycles': json.dumps(cocycles),
        'distance_matrix': json.dumps(result['dperm2all'].tolist()),
    }


@api_rest.route('/upload_data')
class UploadData(Resource):
    def post(self):
        data = request.json

        data_array = np.array(data['points'])
        data_array = data_array.astype(np.float32)

        prime = int(data['prime'])
        cocycles = bool(data['do_cocycles'])

        obj = ndarray_to_object(data_array, 1, prime, cocycles)

        return Response(json.dumps(obj), status=200, headers={'Content-Type': 'application/json'})
