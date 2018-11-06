import time

from flask import session
from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.specs.rfc6749 import grants
from authlib.specs.rfc6750 import BearerTokenValidator
from authlib.specs.rfc7009 import RevocationEndpoint
from authlib.specs.rfc7519 import jwk
from authlib.specs.rfc7523 import JWTBearerGrant
from authlib.specs.rfc7662 import IntrospectionEndpoint
from werkzeug.security import gen_salt
from project.app.models.user import User
from project.app.models.oauth2 import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token
from project.app.services import oauth2Service, userService
from project.app.services.utils import userUtils
from project.app.web.utils import authUtils, dtoUtils


class _PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'none', 'client_secret_basic', 'client_secret_post'
    ]

    def create_token_response(self):
        client = self.request.client
        token = self.generate_token(
            client, self.GRANT_TYPE,
            user=self.request.user,
            scope=self.request.scope,
        )
        self.server.save_token(token, self.request)
        self.execute_hook('process_token', token=token)
        session['id'] = str(self.request.user.get_user_id())
        return 200, token, self.TOKEN_RESPONSE_HEADER

    def authenticate_user(self, username, password):
        print("PasswordGrant->authenticate_user called: " + str(username))

        user = userService.getUserByUsername(username)
        if(user is not None):
            isPasswordValid = userUtils.isUserValid(user, password)
            if isPasswordValid:
                return user

        return None


class _BearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, tokenString):  
        print("_BearerTokenValidator->authenticate_token called..." + tokenString)
        # oAuth2Token = OAuth2Token()
        # return oAuth2Token
        payload = authUtils.decodeAuthTokenPayload(tokenString)
        print("_BearerTokenValidator->payload:" + str(payload))
        dbToken = oauth2Service.queryToken(payload['jti'], 'access_token')
        print("dbToken:" + str(dbToken))

        #    'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
        #     'iat': datetime.utcnow(),
        #     'sub': user.id,
        #     'jti': str(jtiUuid),
        #     'auth': authorityList

        # item = OAuth2Token()
        # item.client_id=clientId
        # item.user_id=userId
        # item.token_type = tokenType
        # item.scope = scope
        # item.access_token = jti
        # item.revoked = False
        # item.issued_at = issuedAt
        # item.expires_in = expiresIn

        return dbToken

    def request_invalid(self, request):
        print("request_invalid->request:" + str(request))
        return False

    def token_revoked(self, token):
        print("token_revoked:" + str(token))
        return token.revoked

OAUTH2_TOKEN_EXPIRES_IN = {
    'authorization_code': 864000,
    'implicit': 3600,
    'password': 864000,
    'client_credentials': 864000
}

def queryClient(clientId):
    print("queryClient->clientId:" + str(clientId))
    result = oauth2Service.queryClient(clientId)
    print("queryClient->result:" + str(result))
    return result

def saveToken(token, request):
    # print("saveToken->token:" + str(token))
    # print("saveToken->token('access_token'):" + str(token.get('access_token')))
    # print("saveToken->request:" + str(request))
    decodedToken = authUtils.decodeAuthTokenPayload(token.get('access_token'))
    # print("decodedToken:type=" + str(type(decodedToken)))
    # print("decodedToken=" + str(decodedToken))
    # print("jti=" + str(decodedToken['jti']))

    authorities = userUtils.getUserAuthorities(request.user)
    authorityList = dtoUtils.authoritySerialize(authorities)
    scopeList = ' '.join(authorityList)

    clientId = request.client.client_id
    userId = request.user.get_user_id()
    tokenType = token['token_type']
    scope = scopeList
    jti = decodedToken['jti']
    issuedAt = time.time()
    expiresIn = time.time() + token['expires_in']

    # clientId, userId, tokenType, scope, jti, issuedAt, expiresIn
    oauth2Service.saveToken(clientId, userId, tokenType, scope, jti, issuedAt, expiresIn)


def generateJwtToken(client, grant_type, user, scope):
    # print("client:" + str(client))
    # print("grant_type:" + str(grant_type))
    # print("user:" + str(user))
    # print("scope:" + str(scope))

    authorities = userUtils.getUserAuthorities(user)
    token = authUtils.encodeAuthToken(user, authorities)
    # print("token:" + str(token ))

    return token.decode("utf-8")
    


# ------------------------------------------------------------------------------
# Set up the Oauth Server
# ------------------------------------------------------------------------------
print("Creating AuthorizationServer...")
authorizationServer = AuthorizationServer(
    query_client=queryClient,
    save_token=saveToken
)

# supported grants
authorizationServer.register_grant(_PasswordGrant)

# scopes definition
scopes = {
    'public': 'Public Access',
    'admin': 'Admin Access'
}

# protect resource
require_oauth = ResourceProtector()
require_oauth.register_token_validator(_BearerTokenValidator())

def init(app):
    app.config['OAUTH2_ACCESS_TOKEN_GENERATOR'] = generateJwtToken

    print("initializing up AuthorizationServer...")
    authorizationServer.init_jwt_config(app)
    authorizationServer.init_app(app)
