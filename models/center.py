import json
#from models.animal import Animal
from models import db


def get_all_centers():
    return Center.query.all()


def get_center(_center_id):
    return Center.query.filter_by(id=_center_id).first()


def add_center(_login, _password, _address):
    new_center = Center(login=_login, password=_password, address=_address)
    db.session.add(new_center)
    db.session.commit()


class Center(db.Model):
    __tablename__ = "center"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(32))

    animals = db.relationship(
        "Animal",
        backref="center",
        cascade="all, delete, save-update, delete-orphan",
        single_parent=True,
    )

    def __repr__(self):
        center_object = {
            'login': self.login,
            'address': self.address,
            # 'animals': self.animals
        }
        return json.dumps(center_object)


