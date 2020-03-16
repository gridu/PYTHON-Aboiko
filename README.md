# REST API with Flask

The project delivers REST API for Animals Sales. 
Python3 and Flask microframework were chosen as the main tools for the project.
The data persists in SQLite. SQLAlchemy as ORM and plain SQL queries are used for the Data Access layer of the project.
Configparser used to read configuration data from .ini file.
All POST, PUT and DELETE requests are logged in separate file; application logs stored in a dedicated file for it.
Jwt tokens are used for security and identifying users requests.
To validate requests body "flask expect-json" library is used. Hashing algoithm HSA-256 utilized to store user passwords.
Pytest-mocker library was chosen to conduct unit-tests.

## Setup and configure
1) Python 3 is required to properly run the project. You can install it on MacOS with brew package manager:
```
brew install python3
```
2) Clone a project from git repository:
```
git clone https://github.com/gridu/PYTHON-Aboiko
```
The project will be cloned to the directory you run this command from.

3) To separate all project dependencies from OS environment create a virtual environment for the project.
Install a tool to create a virtual environment:
```
pip3 install virtualenv
```
4) To create a directory for virtual environment enter the root project directory and run a command:
```
virtualenv venv
```
5) Activate a virtual environment:
```
source venv/bin/activate
```
6) Collect and install the project dependencies:
```
pi3 install -r requirements.txt
```
## Run project and use API
To run a project type:
```
python run.py
```
from a root project directory

Now you can send requests on a localhost with 5000 port configured by default (http://127.0.0.1:5000/):
| URL         | Result          |
| ---------------|-------------|
| http://127.0.0.1:5000/centers | view all centers|
| http://127.0.0.1:5000/centers/1 | view a center with id 1 as example|
| http://127.0.0.1:5000/species/1 | view the specie with id 1 (if such specie exists)|
| http://127.0.0.1:5000/login | to login with center credentials|

To register a new center send a POST HTTP request tothe following URL. Use schemas.py file as a reference to create request body

http://127.0.0.1:5000/register 

After the user logged in with valid center credentials he recieves a jwt token in a response header from the server, he could perfrom the next GET requests:
| URL         | Result          |
|-------------------|-------------|
| http://127.0.0.1:5000/animals | view all the animals related to the center
| http://127.0.0.1:5000/animals/id | view exact animal taking into account id is one of the animals ids which are related to the center
| http://127.0.0.1:5000/species | view all species

Once jwt token recieved the user logged in with proper center credentials could perform POST, PUT and DELETE
HTTP methods with following URLs:
|   Method     |     URL      | Result |
|-----|---------------------|-----------------|
| POST | http://127.0.0.1:5000/animals/id | added animal with animal data in JSON (to properly create a JSON with animal data please check schemas.py file) |
| PUT | http://127.0.0.1:5000/animals/id | update animal with animal data in JSON |
|DELETE | http://127.0.0.1:5000/animals/1 | delete animal with id 1 as an example |
|POST | http://127.0.0.1:5000/species/id | add a new specie |

Please, not that one could only update, put, delete and view animals related to his center id.

## The project structure
Root folder:

![alt text](https://github.com/gridu/PYTHON-Aboiko/blob/master/miscellaneous/images/Selection_266.png)

Application folder:

![alt text](https://github.com/gridu/PYTHON-Aboiko/blob/master/miscellaneous/images/app_structure.png)
    
Tests folder:

![alt text](https://github.com/gridu/PYTHON-Aboiko/blob/develop/miscellaneous/images/tests_structure.png)

## Run tests
To run all tests please perform the next command from /tests directory:
```
pytest
```
To run single test file specify the path to this file as with command pytest (test_center.py as an example):
```
pytest tests/unit_tests/test_center.py
```
The results of tests run:

![Pytest results](https://github.com/gridu/PYTHON-Aboiko/blob/develop/miscellaneous/images/test_results.png)
