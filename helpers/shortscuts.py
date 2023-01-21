from werkzeug.exceptions import NotFound
#from flask_babel import _


def get_object_or_404(model, obj_id):
    try:
        obj = model.query.get(obj_id)
    except:
        raise NotFound(description=f"with id={obj_id} not found")
    return obj

def get_object_is_not_arhive(model):
    try:
        obj = model.query.filter_by(is_archive=False).one()
    except:
        raise NotFound(description=f"object in arhive")
    return obj