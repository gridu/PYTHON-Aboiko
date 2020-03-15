import json

from application import db


def make_json(self):
    return {
        'id': self.id,
        'login': self.login,
        'address': self.address
    }


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
            'address': self.address
        }
        return json.dumps(center_object)
