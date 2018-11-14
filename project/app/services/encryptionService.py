from urllib import parse
import base64
from cryptography.fernet import Fernet
from project.app.services import commonService


def encrypt_string(plain_text, encrypt_key=None):
    if encrypt_key is None:
        encrypt_key = commonService.get_config_by_key("app_secret_key")

    key = base64.urlsafe_b64encode(encrypt_key.encode())

    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(plain_text.encode())

    return cipher_text


def encrypt_string_with_base64(plain_text, encrypt_key=None):
    cipher_text = encrypt_string(plain_text, encrypt_key)
    base64_text = base64.urlsafe_b64encode(cipher_text)

    return base64_text


def encrypt_dictionary(dictionary, encrypt_key=None):
    dict_string = parse.urlencode(dictionary, encrypt_key)
    cipher_text = encrypt_string(dict_string)

    return cipher_text


def encrypt_dictionary_with_base64(dictionary, encrypt_key=None):
    cipher_text = encrypt_dictionary(dictionary, encrypt_key)
    base64_text = base64.urlsafe_b64encode(cipher_text)

    return base64_text


def decrypt_string(cipher_text, encrypt_key=None):
    if encrypt_key is None:
        encrypt_key = commonService.get_config_by_key("app_secret_key")

    key = base64.urlsafe_b64encode(encrypt_key.encode())

    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode('UTF-8')

    return plain_text


def decrypt_string_with_base64(base64_text, encrypt_key=None):
    cipher_text = base64.urlsafe_b64decode(base64_text)
    return decrypt_string(cipher_text, encrypt_key)


def decrypt_dictionary(cipher_text, encrypt_key=None):
    plain_text = decrypt_string(cipher_text, encrypt_key)
    parsed_list = parse.parse_qsl(plain_text)
    dictionary = {}

    for r in parsed_list:
        key = r[0]
        value = r[1]
        dictionary[key] = value

    return dictionary


def decrypt_dictionary_with_base64(base64_text, encrypt_key=None):
    cipher_text = base64.urlsafe_b64decode(base64_text)
    return decrypt_dictionary(cipher_text, encrypt_key)
