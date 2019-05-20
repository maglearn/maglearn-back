from flask_restplus import Resource, fields

from maglearn_back.api.restplus import api
from maglearn_back.library.networks import NetworkType

ns = api.namespace("networks", description="CRUD operations on Networks")

network_type_schema = api.model('Network Type', {
    "name": fields.String(description="Network type name.")
})


@ns.route("/types")
class NetworkTypeCollection(Resource):

    @ns.marshal_with(network_type_schema)
    def get(self):
        """List of available network types."""
        return [t for t in NetworkType]
