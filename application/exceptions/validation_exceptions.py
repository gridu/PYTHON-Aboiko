class AnimalExistsException(ValueError):
    """Raised when center wants to add existing animal"""
    pass


class AnimalNotFoundException(ValueError):
    """Raised when center wants to add existing animal"""
    pass


class IncorrectCredentialsException(ValueError):
    """Raised when center representative wants to update or delete an animal which doesn't relate to the center"""
    pass


class CenterDoesNotException(ValueError):
    """Raised when one tries to enter API with not existing login"""
    pass


class SpecieDoesNotExistException(ValueError):
    pass


class CenterAlreadyExistsException(ValueError):
    pass
