from application.models.animal import Animal
from application.models.specie import Specie


# check that db contains specified specie name
def is_specie_exist(_specie):
    return Specie.query.filter_by(name=_specie).one_or_none() is not None


# check that center could perfprm CRUD operations on animal instance
def is_center_id_valid(_center_id, animal):
    return animal.center_id == _center_id


# check that animal instance with the same data is already inserted
def is_there_exact_animal(_center_id, _name, _age, _specie):
    existing_animal = Animal.query.filter(Animal.center_id == _center_id) \
        .filter(Animal.name == _name).filter(Animal.age == _age) \
        .filter(Animal.specie == _specie).one_or_none()
    return existing_animal is not None
