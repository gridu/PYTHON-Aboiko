from passlib.hash import pbkdf2_sha256 as sha256


def generate_hash(password):
    # function to provide a hash to a center password
    return sha256.hash(password)


def verify_hash(password, hash):
    # function to obtain center password from provided hashed data
    return sha256.verify(password, hash)
