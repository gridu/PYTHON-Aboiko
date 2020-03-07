from application import db
from application.exceptions.validation_exceptions import SpecieDoesNotExistException
from application.models.specie import Specie


def add_specie(_name, _price, _description):
    new_specie = Specie(name=_name, price=_price, description=_description)
    db.session.add(new_specie)
    db.session.commit()


def get_specie(_specie_id):
    specie = Specie.query.get(_specie_id)
    if specie is None:
        raise SpecieDoesNotExistException
    return Specie.make_json(specie)


def get_all_species():
    return [Specie.make_json(specie) for specie in Specie.query.all()]