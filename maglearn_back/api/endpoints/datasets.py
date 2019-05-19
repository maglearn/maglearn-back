import math

import petname
from flask import jsonify, request
from flask_restplus import Resource, fields

from maglearn_back import celery
from maglearn_back.api.restplus import api
from maglearn_back.database import db
from maglearn_back.library.data_generation import DampedSineWave, \
    generate_random_fun_samples
from maglearn_back.model import Dataset

ns = api.namespace("datasets", description="CRUD operations on Datasets")


def find():
    datasets = Dataset.query \
        .filter(Dataset.deleted.is_(False)) \
        .order_by(Dataset.id) \
        .all()
    return jsonify(
        [datasetToJson(d)
         for d in datasets])


def datasetToJson(d):
    return {"id": d.id, "name": d.name, "size": d.size,
            "source_function": d.source_function}


dataset_schema = api.model('Dataset', {
    'name': fields.String(description="Dataset name."),
    'size': fields.Integer(
        description="Number of observations in generated dataset."),
})


@ns.route("/")
class DatasetCollection(Resource):

    def get(self):
        """Returns all Datasets."""
        return find()

    @api.response(202, 'Dataset queued for creation.')
    @api.expect(dataset_schema)
    def post(self):
        """Schedules Dataset creation (long task)."""
        result = generate.delay(**request.json)
        result.forget()
        # TODO: 19.05.2019 John - send also href to proper resource
        return {"task": {"id": result.id}}, 202


@ns.route("/<int:id>")
@api.response(404, 'Dataset not found.')
class DatasetItem(Resource):

    def get(self, id):
        """Returns specific Dataset details."""
        return datasetToJson(Dataset.query.get(id))

    @api.response(204, "Dataset deleted.")
    def delete(self, id):
        """Soft delete (mark only) of specific Dataset."""
        dataset = Dataset.query.get(id)
        dataset.deleted = True
        db.session.commit()
        return None, 204


@celery.task
def generate(name, size):
    """Generates new dataset."""
    wave_fun = DampedSineWave()
    x, y = generate_random_fun_samples(wave_fun, size,
                                       (-4 * math.pi, 4 * math.pi),
                                       noise=True)
    dataset_data = {'x': x.tolist(), 'y': y.tolist()}
    if not name:
        name = petname.generate(3)
    dataset = Dataset(name=name, input_size=1, output_size=1, size=size,
                      source_function=wave_fun.latex_repr,
                      data=dataset_data)
    db.session.add(dataset)
    db.session.commit()
    return True
