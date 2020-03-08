from application import db
from application.exceptions.validation_exceptions import SpecieDoesNotExistException, SpecieExistsException
from application.models.specie import make_json
from application.models.specie import Specie


def add_specie(_name, _price, _description):
    new_specie = Specie(name=_name, price=_price, description=_description)
    is_specie_exist(_name)
    db.session.add(new_specie)
    db.session.commit()
    return make_json(new_specie)


def get_specie(_specie_id):
    specie = Specie.query.get(_specie_id)
    if specie is None:
        raise SpecieDoesNotExistException
    return make_json(specie)


def get_all_species():
    return [make_json(specie) for specie in Specie.query.all()]


def is_specie_exist(_name):
    if Specie.query.filter_by(name=_name).one_or_none() is not None:
        raise SpecieExistsException
