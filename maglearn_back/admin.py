import inspect

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from maglearn_back import model
from maglearn_back.database import db


def _get_model_entities():

    def is_entity(obj):
        return inspect.isclass(obj) and issubclass(obj, db.Model)

    return inspect.getmembers(model, is_entity)


def _add_model_views(admin_):

    class MyModelView(ModelView):
        column_formatters = {
            'data': lambda v, c, m, n: f"{str(m.data)[:100]}..."
        }

    for name, obj in _get_model_entities():
        admin_.add_view(MyModelView(obj, db.session))


admin = Admin(None, 'maglearn-back', template_mode='bootstrap3')


def init_app(app):
    _add_model_views(admin)
    admin.init_app(app)
