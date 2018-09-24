import string, hashlib, binascii
from random import randint
from random import choice
from random import SystemRandom
from services.utils.securityUtils import constants




def randomUserPrivateKey(maxSize):
    allchar = string.ascii_letters + string.digits
    rand = "".join(SystemRandom().choice(allchar) for x in range(maxSize))
 

    return rand

def randomString(min_char, max_char):
    allchar = string.ascii_letters + string.digits
    rand = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    
    return rand

def is_user_valid(user, password):
    if(user is None):
        return None

    tmp_hashed_password = get_hashed_password(password, user.password_salt)
    if(tmp_hashed_password == user.password_hash):
        return True
    else:
        return False


def get_hashed_password(password, userSalt):
    applicationSalt = constants["APP_PASSWORD_SALT"]
    iterations = constants["APP_PASSWORD_HASH_ITERATIONS"]
    dk = hashlib.pbkdf2_hmac("sha512", 
                                        bytearray(password.encode('utf-8') + applicationSalt.encode('utf-8')), 
                                        bytearray(userSalt.encode('utf-8')), 
                                        iterations)
    hexdigest = binascii.hexlify(dk).decode('utf-8')

    return hexdigest    