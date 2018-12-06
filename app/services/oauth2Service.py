
from app.persist import oauth2Dao, baseDao


def add_authorization_code(client, user, request):
    session = baseDao.get_session()
    return oauth2Dao.add_authorization_code(session, client, user, request)


def parse_authorization_code(code, client):
    session = baseDao.get_session()
    return oauth2Dao.parse_authorization_code(session, code, client)


def delete_authorization_code(authorization_code):
    session = baseDao.get_session()
    return oauth2Dao.delete_authorization_code(session, authorization_code)


def authenticate_user(authorization_code):
    session = baseDao.get_session()
    return oauth2Dao.authenticate_user(session, authorization_code)


def query_client(client_id):
    session = baseDao.get_session()
    return oauth2Dao.query_client(session, client_id)


def query_token(token, token_type_hint):
    session = baseDao.get_session()
    return oauth2Dao.query_token(session, token, token_type_hint)


def save_token(client_id, user_id, token_type, scope, jti, issued_at, expires_in):
    session = baseDao.get_session()
    return oauth2Dao.save_token(session, client_id, user_id, token_type, scope, jti, issued_at, expires_in)
