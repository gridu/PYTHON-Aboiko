import json

from flask import jsonify, Response, make_response

from application import db
from application.exceptions.validation_exceptions import SpecieDoesNotExistException, SpecieExistsException
from application.models.specie import make_json
from application.models.specie import Specie


def add_specie(_name, _price, _description):
    """
    This function responds to POST request to /species and creates a new specie

    :param _description:    description of the specie from request (string)
    :param _price:          price of the specie from request (integer)
    :param _name:           name of the specie from request (string)
    :return:                JSON of created specie data on success
    """
    specie = Specie(name=_name, price=_price, description=_description)
    if specie_exist(_name):
        msg = 'That specie already exists'
        return make_response(jsonify({"error": msg}), 409)
    db.session.add(specie)
    db.session.commit()
    new_specie = make_json(specie)
    specie_id = new_specie['specie_id']
    response = Response(
        response=json.dumps(new_specie),
        status=201,
        mimetype='application/json'
    )
    response.headers['Location'] = "/species/{0}".format(str(specie_id))
    return response



def get_specie(_specie_id):
    """
    This function responds to a GET request for /species/{specie_id}
    with one matching specie

    :param _specie_id:         Id of the specie
    :return:                json string of specie contents
    """
    specie = Specie.query.get(_specie_id)
    if specie is None:
        msg = 'Specie you\'re looking for doesn\'t exist'
        return jsonify({"error": msg}), 404
    return make_json(specie)




def get_all_species():
    """
    This function responds to a GET request for /species
    with the complete list of species

    :return:                json list with all species
    """
    return make_response(jsonify({'species':
                        [make_json(specie) for specie in Specie.query.all()]}), 200)


def specie_exist(_name):
    return Specie.query.filter_by(name=_name).one_or_none() is not None
