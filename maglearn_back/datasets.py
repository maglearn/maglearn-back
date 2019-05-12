import math
from flask import Blueprint, request, render_template

from maglearn_back.database import db
from maglearn_back.library.data_generation import generate_random_fun_samples, \
    DampedSineWave
from maglearn_back.model import Dataset
from maglearn_back.tasks import celery

bp = Blueprint('datasets', __name__, url_prefix='/datasets')


@bp.route("/", methods=['GET'])
def list():
    datasets = Dataset.query.order_by(Dataset.id).all()
    return render_template('datasets/list.html', datasets=datasets)


@bp.route("/start_generation", methods=['POST'])
def start_generation():
    """Starts dataset generation job with given parameters."""
    if request.method == 'POST':
        size = request.form.get('size', type=int)
        result = generate.delay(size)
        result.forget()
        return "ok"
    return "error"


@celery.task
def generate(dataset_size):
    """Generates new dataset."""
    wave_fun = DampedSineWave()
    x, y = generate_random_fun_samples(wave_fun, dataset_size,
                                       (-4 * math.pi, 4 * math.pi),
                                       noise=True)
    dataset_data = {'x': x.tolist(), 'y': y.tolist()}
    dataset = Dataset(input_size=1, output_size=1, size=dataset_size,
                      source_function=wave_fun.latex_repr,
                      data=dataset_data)
    db.session.add(dataset)
    db.session.commit()
    return True
