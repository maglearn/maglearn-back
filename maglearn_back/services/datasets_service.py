import math
import petname

from maglearn_back import celery
from maglearn_back.database import db
from maglearn_back.library.data_generation import DampedSineWave, \
    generate_random_fun_samples
from maglearn_back.model import Dataset


def get_all():
    return Dataset.query \
        .filter(Dataset.deleted.is_(False)) \
        .order_by(Dataset.id) \
        .all()


def find_by_id(id):
    return Dataset.query.get(id)


def delete(id):
    dataset = Dataset.query.get(id)
    if dataset is None:
        return False
    dataset.deleted = True
    db.session.commit()
    return True


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
