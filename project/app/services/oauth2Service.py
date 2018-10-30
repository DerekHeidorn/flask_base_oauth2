from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from project.app.models.oauth2 import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token
from project.app.persist import oauth2Dao

queryClientFunction = create_query_client_func(oauth2Dao.getSession(), OAuth2Client)
saveTokenFunction = create_save_token_func(oauth2Dao.getSession(), OAuth2Token)
revocationEndpoint = create_revocation_endpoint(oauth2Dao.getSession(), OAuth2Token)
bearerTokenValidator = create_bearer_token_validator(oauth2Dao.getSession(), OAuth2Token)

def addAuthorizationCode(client, user, request):
    return oauth2Dao.addAuthorizationCode(client, user, request)

def parseAuthorizationCode(code, client):
    return oauth2Dao.parseAuthorizationCode(code, client)

def deleteAuthorizationCode(authorizationCode):
    return oauth2Dao.deleteAuthorizationCode(authorizationCode)

def authenticateUser(authorizationCode):
    return oauth2Dao.authenticateUser(authorizationCode)




    # protect resource
