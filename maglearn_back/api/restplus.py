import logging
import importlib

from flask import Blueprint
from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(version="0.1.0", title="maglearn-back API")


def init_app(flask_app):
    """Creates blueprint to host API and adds namespaces."""
    log.info("Initializing RESTPlus.")
    bp = Blueprint('api', __name__, url_prefix="/api")
    api.init_app(bp)
    endpoints = ["datasets"]
    # must be loaded dynamically to avoid circular dependency
    for endpoint in endpoints:
        importlib.import_module("maglearn_back.api.endpoints." + endpoint)
    flask_app.register_blueprint(bp)
