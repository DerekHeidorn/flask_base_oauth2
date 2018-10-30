from project.app.persist.baseDao import getSession
from project.app.models.oauth2 import OAuth2AuthorizationCode
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
    session.add(item)
    session.commit()
    return code

def parseAuthorizationCode(code, client):
    session = getSession()
    item = session.query(OAuth2AuthorizationCode).filter(
        code=code, client_id=client.client_id).first()

    if item and not item.is_expired():
        return item

def deleteAuthorizationCode(authorizationCode):
    session = getSession()
    session.delete(authorizationCode)
    session.commit()

def authenticateUser(authorizationCode):
    session = getSession()
    user = session.query(User).filter(User.id == authorizationCode.userId).first()
    return user 
