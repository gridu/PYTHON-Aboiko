register_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string'},
        'password': {'type': 'string'},
        'address': {'type': 'string'}
    },
    'required': ['login', 'password', 'address']
}

login_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['login', 'password']
}

post_animal_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'age': {'type': 'number'},
        'specie': {'type': 'string'}
    },
    'required': ['name', 'age', 'specie']
}

post_specie_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'price': {'type': 'number'},
        'description': {'type': 'string'}
    },
    'required': ['name', 'price', 'description']
}

put_animal_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'age': {'type': 'number'},
        'specie': {'type': 'string'}
    }
}
