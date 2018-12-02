
from app.persist import oauth2Dao


def add_authorization_code(client, user, request):
    return oauth2Dao.add_authorization_code(client, user, request)


def parse_authorization_code(code, client):
    return oauth2Dao.parse_authorization_code(code, client)


def delete_authorization_code(authorization_code):
    return oauth2Dao.delete_authorization_code(authorization_code)


def authenticate_user(authorization_code):
    return oauth2Dao.authenticate_user(authorization_code)


def query_client(client_id):
    return oauth2Dao.query_client(client_id)


def query_token(token, token_type_hint):
    return oauth2Dao.query_token(token, token_type_hint)


def save_token(client_id, user_id, token_type, scope, jti, issued_at, expires_in):
    return oauth2Dao.save_token(client_id, user_id, token_type, scope, jti, issued_at, expires_in)
