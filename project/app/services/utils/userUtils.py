import string
import hashlib
import binascii
from random import randint
from random import choice
from random import SystemRandom
from project.app.services.utils.securityUtils import constants


def random_user_private_key(max_size):
    all_char = string.ascii_letters + string.digits
    rand = "".join(SystemRandom().choice(all_char) for x in range(max_size))

    return rand


def random_string(min_char, max_char):
    all_char = string.ascii_letters + string.digits
    rand = "".join(choice(all_char) for x in range(randint(min_char, max_char)))
    
    return rand


def is_user_valid(user, password):
    if user is None:
        return False

    tmp = get_hashed_password(password, user.password_salt)

    if tmp.strip() == user.password_hash.strip():
        return True
    else:
        return False


def get_hashed_password(password, user_salt):
    application_salt = constants["APP_PASSWORD_SALT"]
    iterations = constants["APP_PASSWORD_HASH_ITERATIONS"]
    dk = hashlib.pbkdf2_hmac("sha512", 
                             bytearray(password.encode('utf-8') + application_salt.encode('utf-8')),
                             bytearray(user_salt.encode('utf-8')),
                             iterations)
    hex_digest = binascii.hexlify(dk).decode('utf-8')

    return hex_digest


def get_user_authorities(user):
    authorities = []

    if user is not None and user.security_groups is not None:
        for sg in user.security_groups:
            if sg is not None:
                for sa in sg.authorities:
                    authorities.append(sa)
            
    return authorities
