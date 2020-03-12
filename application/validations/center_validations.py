from application.models.center import Center
from application.util import verify_hash


# function that returns True center exists
def does_exist(_login):
    center = find_by_login(_login)
    return center is not None


# function that returns True if specified combination of center login and password exists
def validate_credentials(_login, _password):
    center = find_by_login(_login)
    if center is None:
        return False
    valid_pas = verify_hash(_password, center.password)
    return valid_pas


# helper function to find center by its login
def find_by_login(_login):
    return Center.query.filter_by(login=_login).first()
