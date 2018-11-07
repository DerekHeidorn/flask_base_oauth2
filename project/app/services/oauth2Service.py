
from project.app.persist import oauth2Dao


def addAuthorizationCode(client, user, request):
    return oauth2Dao.addAuthorizationCode(client, user, request)


def parseAuthorizationCode(code, client):
    return oauth2Dao.parseAuthorizationCode(code, client)


def deleteAuthorizationCode(authorizationCode):
    return oauth2Dao.deleteAuthorizationCode(authorizationCode)


def authenticateUser(authorizationCode):
    return oauth2Dao.authenticateUser(authorizationCode)


def createAccessToken(token, client, grantUser=None):
    return oauth2Dao.createAccessToken(token, client, grantUser)


def getOAuth2Clients(userId):
    return oauth2Dao.getOAuth2Clients(userId)


def queryClient(clientId):
    return oauth2Dao.queryClient(clientId)


def queryToken(token, tokenTypeHint):
    print("oauth2Service->queryToken called...")
    return oauth2Dao.queryToken(token, tokenTypeHint)


def saveToken(clientId, userId, tokenType, scope, jti, issuedAt, expiresIn):
    return oauth2Dao.saveToken(clientId, userId, tokenType, scope, jti, issuedAt, expiresIn)
