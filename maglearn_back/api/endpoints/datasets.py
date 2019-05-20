from flask import request
from flask_restplus import Resource, fields

from maglearn_back.api.restplus import api
from maglearn_back.services import datasets_service

ns = api.namespace("datasets", description="CRUD operations on Datasets")


dataset_schema = ns.model('Dataset', {
    'id': fields.Integer(description="Dataset unique id."),
    'name': fields.String(description="Dataset name."),
    'size': fields.Integer(
        description="Number of observations in generated dataset."),
    'source_function': fields.String(
        description="Source function representation used for dataset.")
})

dataset_creation_schema = ns.model('Dataset Creation', {
    'name': fields.String(description="Dataset name."),
    'size': fields.Integer(
        description="Number of observations in generated dataset."),
})


@ns.route("/")
class DatasetCollection(Resource):

    @ns.marshal_with(dataset_schema)
    def get(self):
        """Returns all Datasets."""
        return datasets_service.get_all()

    @ns.response(202, 'Dataset queued for creation.')
    @ns.expect(dataset_creation_schema)
    def post(self):
        """Schedules Dataset creation (long task)."""
        result = datasets_service.generate.delay(**request.json)
        result.forget()
        # TODO: 19.05.2019 John - send also href to proper resource
        return {"task": {"id": result.id}}, 202


@ns.route("/<int:id>")
@ns.response(404, 'Dataset not found.')
class DatasetItem(Resource):

    @ns.marshal_with(dataset_schema)
    def get(self, id):
        """Returns specific Dataset details."""
        return datasets_service.find_by_id(id) or (None, 404)

    @ns.response(204, "Dataset deleted.")
    def delete(self, id):
        """Soft delete (mark only) of specific Dataset."""
        return (None, 204) if datasets_service.delete(id) else (None, 404)
