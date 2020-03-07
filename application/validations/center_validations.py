
from application.exceptions.validation_exceptions import IncorrectCredentialsException, CenterDoesNotException
from application.logic.center_logic import find_by_login
from application.util import verify_hash


def does_exist(_login):
    center = find_by_login(_login)
    if center is None:
        raise CenterDoesNotException


def validate_credentials(_login, _password):
    center = find_by_login(_login)
    if center is None:
        return False
    # valid_pas = (center.password == _password)
    valid_pas = verify_hash(_password, center.password)
    if not valid_pas:
        raise IncorrectCredentialsException
