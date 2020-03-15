# REST API with Flask

Created REST API for Animals Sales Web Project.
Flask, SQLite, SQLAlchemy, configparser and logging, jwt tokens, json validations, password hashing,
mocking functions, pytest were used on the project.

## Setup and configure
1) Python 3 is required to properly run the project. You can install it on MacOS with brew package manager:
brew install python3

2) Clone a project from git repository:
git clone https://github.com/gridu/PYTHON-Aboiko

The project will be cloned to the directory you run this command from.

3) To separate all project dependencies from OS environment create a virtual environment for the project.
Install a tool to create a virtual environment:
pip3 install virtualenv

4) To create a directory for virtual environment enter the root project directory and run a command:
virtualenv venv

5) Activate a virtual environment:
source venv/bin/activate

6) Collect and install the project dependencies:
pi3 install -r requirements.txt

## Run project and use API
To run a project type
python run.py
from a root project directory

Now you can send requests on a localhost with 5000 port configured by default (http://127.0.0.1:5000/):
http://127.0.0.1:5000/centers - view all centers
http://127.0.0.1:5000/centers/1 - view a center with id 1 as example
http://127.0.0.1:5000/species/1 - view the specie with id 1 (if such specie exists)
http://127.0.0.1:5000/login - to login with center credentials

To register a new center send a POST HTTP request to
http://127.0.0.1:5000/register (please use schemas.py file as a reference to create request body)

After the user logged in with valid center credentials he recieves a jwt token in a response header from the server, he could perfrom the next GET requests:
http://127.0.0.1:5000/animals - view all the animals related to the center
http://127.0.0.1:5000/animals/id - view exact animal taking into account id is one of the animals ids which are related to the center
http://127.0.0.1:5000/species - view all species

Once jwt token recieved the user logged in with proper center credentials could perform POST, PUT and DELETE
HTTP methods with following URLs:
POST http://127.0.0.1:5000/animals/id - added animal with animal data in JSON (to properly create a JSON with animal data please check schemas.py file)
PUT http://127.0.0.1:5000/animals/id - update animal with animal data in JSON
DELETE http://127.0.0.1:5000/animals/1 - delete animal with id 1 as an example
Please, not that one could only update, put, delete and view animals related to his center id.

POST http://127.0.0.1:5000/species/id - add a new specie (jwt token required for that)

## The project structure
Root folder:

![alt text](https://github.com/gridu/PYTHON-Aboiko/blob/master/miscellaneous/images/Selection_266.png)

Application folder:

![alt text](https://github.com/gridu/PYTHON-Aboiko/blob/master/miscellaneous/images/app_structure.png)
    
Tests folder:

![alt text](https://github.com/gridu/PYTHON-Aboiko/blob/develop/miscellaneous/images/tests_structure.png)

The results of tests run:

![Pytest results](https://github.com/gridu/PYTHON-Aboiko/blob/develop/miscellaneous/images/test_results.png)
