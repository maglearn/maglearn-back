from flask import Blueprint, render_template

from maglearn_back.model import Dataset

bp = Blueprint('datasets', __name__, url_prefix='/datasets')


@bp.route("/", methods=['GET'])
def list():
    datasets = Dataset.query.order_by(Dataset.id).all()
    return render_template('datasets/list.html', datasets=datasets)
