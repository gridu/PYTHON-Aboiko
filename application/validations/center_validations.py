from application.models.center import Center
from application.util import verify_hash


def does_exist(_login):
    center = find_by_login(_login)
    return center is not None  # center exists


def validate_credentials(_login, _password):
    center = find_by_login(_login)
    if center is None:
        return False
    valid_pas = verify_hash(_password, center.password)
    return valid_pas


def find_by_login(_login):
    return Center.query.filter_by(login=_login).one_or_none()
