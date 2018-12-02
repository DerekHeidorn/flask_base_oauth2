import hashlib
from app import core


def hexdigest(input_string, password=None):
    if password is None:
        password = core.global_config["APP_SHARED_SECRET_KEY"]

    return hashlib.sha256(bytearray(input_string.encode('utf-8') + password.encode('utf-8'))).hexdigest()
