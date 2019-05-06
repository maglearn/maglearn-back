import math
from flask import Blueprint, request, render_template

from maglearn_back.tasks import celery
from maglearn_back.database import db
from maglearn_back.library.data_generation import generate_random_fun_samples, \
    DampedSineWave
from maglearn_back.model import Dataset

bp = Blueprint('datasets', __name__, url_prefix='/datasets')


@bp.route("/create", methods=['GET'])
def create():
    return render_template('datasets/create.html')


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
    x, y = generate_random_fun_samples(DampedSineWave(), dataset_size,
                                       (-4 * math.pi, 4 * math.pi),
                                       noise=True)
    dataset1_data = {'x': x.tolist(), 'y': y.tolist()}
    dataset1 = Dataset(input_size=1, output_size=1, size=dataset_size,
                       source_function='exp(-lambda*x") * cos(omega *x * phi)',
                       data=dataset1_data)
    db.session.add(dataset1)
    db.session.commit()
    return True
