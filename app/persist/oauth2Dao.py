

from app.persist import baseDao
from app.models.oauth2 import OAuth2AuthorizationCode, OAuth2Token, OAuth2Client
from app.models.user import User
from werkzeug.security import gen_salt


def add_authorization_code(client, user, request):
    session = baseDao.get_session()

    code = gen_salt(48)
    item = OAuth2AuthorizationCode()
    item.code = code
    item.client_id = client.client_id
    item.redirect_uri = request.redirect_uri
    item.scope = request.scope
    item.user_id = user.user_id

    session.add(item)
    session.commit()
    return code


def parse_authorization_code(code, client):

    session = baseDao.get_session()
    item = session.query(OAuth2AuthorizationCode).filter(
        OAuth2AuthorizationCode.code == code,
        OAuth2AuthorizationCode.client_id == client.client_id).first()

    if item and not item.is_expired():
        return item


def delete_authorization_code(authorization_code):
    session = baseDao.get_session()
    session.delete(authorization_code)
    session.commit()


def authenticate_user(authorization_code):
    session = baseDao.get_session()
    user = session.query(User).filter(User.user_id == authorization_code.user_id).first()
    return user 


def query_client(client_id, session=None):

    if session is None:
        session = baseDao.get_session()
    oauth2_client = session.query(OAuth2Client).filter(OAuth2Client.client_id == client_id).first()

    return oauth2_client


def query_token(token, token_type_hint):
    session = baseDao.get_session()

    if token_type_hint == 'access_token':
        return session.query(OAuth2Token).filter(OAuth2Token.access_token == token).first()
    elif token_type_hint == 'refresh_token':
        return session.query(OAuth2Token).filter(OAuth2Token.refresh_token == token).first()
    # without token_type_hint
    item = session.query(OAuth2Token).filter(OAuth2Token.access_token == token).first()
    if item:
        return item
    return session.query(OAuth2Token).filter(OAuth2Token.refresh_token == token).first()


def save_token(client_id, user_id, token_type, scope, jti, issued_at, expires_in):
    item = OAuth2Token()
    item.client_id = client_id
    item.user_id = user_id
    item.token_type = token_type
    item.scope = scope
    item.access_token = jti
    item.revoked = False
    item.issued_at = issued_at
    item.expires_in = expires_in
    
    session = baseDao.get_session()
    session.add(item)
    session.commit()

    return item
