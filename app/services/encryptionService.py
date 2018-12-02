from urllib import parse
import base64
from cryptography.fernet import Fernet
from project.app import core


def encrypt(data, encrypt_key=None):
    if encrypt_key is None:
        encrypt_key = core.global_config["APP_SECRET_KEY"]

    key = base64.urlsafe_b64encode(encrypt_key.encode())

    cipher_suite = Fernet(key)
    cipher_output = cipher_suite.encrypt(data)

    return cipher_output


def encrypt_string(data_string, encrypt_key=None):
    if encrypt_key is None:
        encrypt_key = core.global_config["APP_SECRET_KEY"]

    key = base64.urlsafe_b64encode(encrypt_key.encode())

    cipher_suite = Fernet(key)
    cipher_output = cipher_suite.encrypt(data_string.encode()).decode('UTF-8')

    return cipher_output


def encrypt_string_with_base64(plain_text, encrypt_key=None):
    cipher_output = encrypt(plain_text.encode(), encrypt_key)
    base64_text = base64.urlsafe_b64encode(cipher_output).decode('UTF-8')

    return base64_text


def encrypt_dictionary(dictionary, encrypt_key=None):
    dict_string = parse.urlencode(dictionary)
    cipher_output = encrypt(dict_string.encode(), encrypt_key)

    return cipher_output.decode('UTF-8')


def encrypt_dictionary_with_base64(dictionary, encrypt_key=None):
    cipher_text = encrypt_dictionary(dictionary, encrypt_key)
    base64_text = base64.urlsafe_b64encode(cipher_text.encode()).decode('UTF-8')

    return base64_text


def decrypt(cipher_data, encrypt_key=None):
    if encrypt_key is None:
        encrypt_key = core.global_config["APP_SECRET_KEY"]

    key = base64.urlsafe_b64encode(encrypt_key.encode())

    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(cipher_data)

    return decrypted_data


def decrypt_string(cipher_text, encrypt_key=None):

    plain_text = decrypt(cipher_text.encode(), encrypt_key).decode('UTF-8')

    return plain_text


def decrypt_string_with_base64(base64_text, encrypt_key=None):
    cipher_text = base64.urlsafe_b64decode(base64_text)
    return decrypt(cipher_text, encrypt_key).decode('UTF-8')


def decrypt_dictionary(cipher_text, encrypt_key=None):
    decrypted = decrypt(cipher_text.encode(), encrypt_key)
    parsed_list = parse.parse_qsl(decrypted.decode('UTF-8'))
    dictionary = {}

    for r in parsed_list:
        key = r[0]
        value = r[1]
        dictionary[key] = value

    return dictionary


def decrypt_dictionary_with_base64(base64_text, encrypt_key=None):
    cipher_bytes = base64.urlsafe_b64decode(base64_text.encode())
    decrypted = decrypt(cipher_bytes, encrypt_key)
    parsed_list = parse.parse_qsl(decrypted.decode('UTF-8'))
    dictionary = {}

    for r in parsed_list:
        key = r[0]
        value = r[1]
        dictionary[key] = value

    return dictionary
