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

def saveToken(token, request):

    print("----------------------------------------------------------")
    print("saveToken->token=" + str(type(token)) + " " + str(token))
    print("saveToken->request=" +  str(type(request)) + " " + str(request))
    print("saveToken->self.user=" +  str(type(request.user)) + " " + str(request.user))
    print("saveToken->self.client=" +  str(type(request.client)) + " " + str(request.client.client_id))

    #  client_id = Column(String(48))
    # token_type = Column(String(40))
    # access_token = Column(String(255), unique=True, nullable=False)
    # refresh_token = Column(String(255), index=True)
    # scope = Column(Text, default='')
    # revoked = Column(Boolean, default=False)
    # issued_at = Column(
    #     Integer, nullable=False, default=lambda: int(time.time())
    # )
    # expires_in = Column(Integer, nullable=False, default=0)

    # if request.user:
    #     user_id = request.user.get_user_id()
    #     return
    # else:
    #     # client_credentials grant_type
    #     user_id = request.client.user_id
    #     # or, depending on how you treat client_credentials
    #     user_id = None

    item = OAuth2Token()
    item.client_id=request.client.client_id
    item.user_id=request.user.get_user_id()
    item.token_type = token['token_type']
    item.scope = 'profile'
    item.access_token = token['access_token']
    item.revoked = False
    item.issued_at = time.time()
    item.expires_in = time.time() + token['expires_in']
    
    session = getSession()
    session.add(item)
    session.commit()