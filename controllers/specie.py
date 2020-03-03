import config
from flask import *
from models.specie import *

@app.route('/species')
def get_species():
    return jsonify({'species': Specie.get_all_species()})