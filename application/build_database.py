import os

# from . import db, create_app
from application.animal import Animal
from application.center import Center
from application.specie import Specie
from application.util import generate_hash


def db_load_example_data(app, db):
    with app.app_context():
        CENTER = [
            {
                "login": "Center1",
                "password": "password1",
                "address": "some street, 1",
                "animals": [
                    ("fox1", 2, "red fox"),
                    ("tiger1", 3, "angry tiger"),
                    ("lion1", 1, "giant lion"),
                ],
            },
            {
                "login": "Center2",
                "password": "password2",
                "address": "some street, 2",
                "animals": [
                    ("fox2", 2, "red fox"),
                    ("tiger2", 3, "angry tiger"),
                    ("lion2", 1, "giant lion"),
                ],
            },
            {
                "login": "Center3",
                "password": "password3",
                "address": "some street, 3",
                "animals": [
                    ("fox3", 2, "red fox"),
                    ("tiger3", 3, "angry tiger"),
                    ("lion3", 1, "giant lion"),
                ],
            },
        ]

        SPECIE = [
            {
                "name": "red fox",
                "price": 12.55,
                "description": "lives in forest"
            },
            {
                "name": "angry tiger",
                "price": 9999999.99,
                "description": "very angry"
            }
        ]

        # iterate over the CENTER structure and populate the database
        for center in CENTER:
            c = Center(login=center.get("login"), password=generate_hash(center.get("password")),
                                   address=center.get("address"))

            for animal in center.get("animals"):
                name, age, specie = animal
                c.animals.append(
                    Animal(
                        name=name,
                        age=age,
                        specie=specie
                    )
                )
            db.session.add(c)

        for specie in SPECIE:
            s = Specie(name=specie.get("name"), price=specie.get("price"),
                                   description=specie.get("description"))
            db.session.add(s)

        db.session.commit()


# if __name__ == "__main__":
#     app = create_app()
#     dat = db
#     db_load_example_data(app, db)
