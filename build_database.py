import os
from config import db
from models.center import Center
from models.animal import Animal
from models.specie import Specie

# Data to initialize database with
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

SPICIE = [
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

# Delete database file if it exists currently
if os.path.exists("sale_animal.db"):
    os.remove("sale_animal.db")

# Create the database
db.create_all()

# iterate over the CENTER structure and populate the database
for center in CENTER:
    c = Center(login=center.get("login"), password=center.get("password"),
               address=center.get("address"))


    for animal in center.get("animals"):
        name, age, spicie = animal
        c.animals.append(
            Animal(
                name=name,
                age=age,
                spicie=spicie
            )
        )
    db.session.add(c)

for spicie in SPICIE:
    s = Specie(name=spicie.get("name"), price=spicie.get("price"),
               description=spicie.get("description"))
    db.session.add(s)

db.session.commit()
