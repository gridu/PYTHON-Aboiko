# REST API with Flask

Created REST API for Animals Sales Web Project.
Flask, SQLite, SQLAlchemy, configparser and logging, jwt tokens, json validations, password hashing,
mocking functions, pytest were used on the project.

The project structure. Application folder:
├── authentification
│   ├── accessrequest.py
│   ├── auth_logic.py
│   └── __init__.py
├── build_database.py
├── custom_logger.py
├── __init__.py
├── logic
│   ├── animal_logic.py
│   ├── center_logic.py
│   ├── __init__.py
│   └── specie_logic.py
├── models
│   ├── animal.py
│   ├── center.py
│   ├── __init__.py
│   └── specie.py
├── routes
│   ├── __init__.py
│   ├── routes_animals.py
│   ├── routes_centers.py
│   └── routes_species.py
├── run.py
├── schemas.py
├── util.py
└── validations
    ├── animal_specie_validations.py
    ├── center_validations.py
    └── __init__.py
    
The project structure. Tests folder:
├── conftest.py
├── __init__.py
├── integration_tests
│   ├── __init__.py
│   ├── test_animal_requests.py
│   ├── test_center_requests.py
│   └── test_specie_requests.py
├── test_data.py
└── unit_tests
    ├── test_animal.py
    ├── test_center.py
    └── test_specie.py

