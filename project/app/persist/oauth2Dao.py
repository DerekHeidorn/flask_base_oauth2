import time

from project.app.persist.baseDao import getSession
from project.app.models.oauth2 import OAuth2AuthorizationCode, OAuth2Token, OAuth2Client
from project.app.models.user import User
from werkzeug.security import gen_salt



def addAuthorizationCode(client, user, request):
    session = getSession()

    code = gen_salt(48)
    item = OAuth2AuthorizationCode(
        code=code,
        client_id=client.client_id,
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        user_id=user.id,
    )
    print("addAuthorizationCode->item=" + str(item))
    session.add(item)
    session.commit()
    return code

def parseAuthorizationCode(code, client):
    print("parseAuthorizationCode->code=" + code)
    print("parseAuthorizationCode->client.client_id=" + client.client_id)
    session = getSession()
    item = session.query(OAuth2AuthorizationCode).filter(
        OAuth2AuthorizationCode.code==code, 
        OAuth2AuthorizationCode.client_id==client.client_id).first()

    if item and not item.is_expired():
        return item

def deleteAuthorizationCode(authorizationCode):
    session = getSession()
    session.delete(authorizationCode)
    session.commit()

def authenticateUser(authorizationCode):
    session = getSession()
    print("authorizationCode.userId=" + authorizationCode.userId)
    user = session.query(User).filter(User.id == authorizationCode.userId).first()
    return user 


def createAccessToken(token, client, grantUser=None):
    userId = client.user_id
    if grantUser is not None:
        userId=grantUser.id

    item = OAuth2Token(
        client_id=client.client_id,
        user_id=userId,
        **token
    )
    session = getSession()
    session.add(item)
    session.commit()

def getOAuth2Clients(userId):
    print("getOAuth2Clients->userId=" + userId)
    session = getSession()
    oauth2Clients = session.query(OAuth2Client).filter(OAuth2Client.user_id==userId).all()
    return oauth2Clients

def _old_queryClient(clientId):
    print("queryClient->clientId=" + clientId)
    session = getSession()
    oauth2Client = session.query(OAuth2Client).filter(OAuth2Client.client_id==clientId).first()
    return oauth2Client

def queryToken(token, tokenTypeHint):
    session = getSession()

    if tokenTypeHint == 'access_token':
        return session.query(OAuth2Token).filter(OAuth2Token.access_token==token).first()
    elif tokenTypeHint == 'refresh_token':
        return session.query(OAuth2Token).filter(OAuth2Token.refresh_token==token).first()
    # without token_type_hint
    item = session.query(OAuth2Token).filter(OAuth2Token.access_token==token).first()
    if item:
        return item
    return session.query(OAuth2Token).filter(OAuth2Token.refresh_token==token).first()

def saveToken(clientId, userId, tokenType, scope, jti, issuedAt, expiresIn):
    item = OAuth2Token()
    item.client_id=clientId
    item.user_id=userId
    item.token_type = tokenType
    item.scope = scope
    item.access_token = jti
    item.revoked = False
    item.issued_at = issuedAt
    item.expires_in = expiresIn
    
    session = getSession()
    session.add(item)
    session.commit()

    return item