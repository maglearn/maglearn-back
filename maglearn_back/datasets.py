import math
from flask import Blueprint, request

from maglearn_back.tasks import celery
from maglearn_back.database import db
from maglearn_back.library.data_generation import generate_random_fun_samples, \
    DampedSineWave
from maglearn_back.model import Dataset

bp = Blueprint('datasets', __name__, url_prefix='/datasets')


@bp.route("/start_generation", methods=['POST'])
def start_generation():
    """Starts dataset generation job with given parameters."""
    if request.method == 'POST':
        result = generate.delay()
        print("Task scheduled. Waiting.")
        result.wait()
        return "ok"
    return "error"


@celery.task
def generate():
    """Generates new dataset."""
    dataset1_size = 150
    x, y = generate_random_fun_samples(DampedSineWave(), dataset1_size,
                                       (-4 * math.pi, 4 * math.pi),
                                       noise=True)
    dataset1_data = {'x': x.tolist(), 'y': y.tolist()}
    dataset1 = Dataset(input_size=1, output_size=1, size=dataset1_size,
                       source_function='exp(-lambda*x") * cos(omega *x * phi)',
                       data=dataset1_data)
    db.session.add(dataset1)
    db.session.commit()
    return True
