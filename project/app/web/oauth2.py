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


class _AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def create_authorization_code(self, client, user, request):
        print("create_authorization_code called...")
        return oauth2Service.addAuthorizationCode(client, user, request)

    def parse_authorization_code(self, code, client):
        print("parse_authorization_code called...")
        return oauth2Service.parseAuthorizationCode(code, client)

    def delete_authorization_code(self, authorizationCode):
        oauth2Service.deleteAuthorizationCode(authorizationCode)

    def authenticate_user(self, authorizationCode):
        print("authenticate_user called...")
        return oauth2Service.authenticateUser(authorizationCode)

class _ImplicitGrant(grants.ImplicitGrant):
    def create_access_token(self, token, client, grant_user):
        oauth2Service.createAccessToken(token, client, grant_user)


class _PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'none', 'client_secret_basic', 'client_secret_post'
    ]

    # def validate_token_request(self):
    #     print("PasswordGrant->validate_token_request called...")
    #     super(_PasswordGrant, self).validate_token_request()

    # def authenticate_token_endpoint_client(self):
    #     print("PasswordGrant->authenticate_token_endpoint_client called...")
    #     super(_PasswordGrant, self).authenticate_token_endpoint_client()

    # def create_token_response(self):
    #     print("PasswordGrant->authenticate_user called...")
    #     super(_PasswordGrant, self).create_token_response()

    def authenticate_user(self, username, password):
        print("PasswordGrant->authenticate_user called: " + str(username))

        user = userService.getUserByLogin(username)
        if(user is not None):
            isPasswordValid = userUtils.isUserValid(user, password)
            if isPasswordValid:
                return user


        return None

class _ClientCredentialsGrant(grants.ClientCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def create_access_token(self, token, client):
        print("ClientCredentialsGrant->create_access_token called...")
        oauth2Service.createAccessToken(token, client)

class _RefreshTokenGrant(grants.RefreshTokenGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_refresh_token(self, refresh_token):
        print("RefreshTokenGrant->authenticate_refresh_token called...")
        item = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.isRefreshTokenExpired():
            return item

    def authenticate_user(self, credential):
        user = userService.getUserById(credential.user_id)
        return user

# class _JWTBearerGrant(JWTBearerGrant):
#     def authenticate_user(self, claims):
#         # get user from claims info, usually it is claims['sub']
#         # for anonymous user, return None
#         return None

#     def authenticate_client(self, claims):
#         # get client from claims, usually it is claims['iss']
#         # since the assertion JWT is generated by this client
#         return get_client_by_iss(claims['iss'])

#     def resolve_public_key(self, headers, payload):
#         # get public key to decode the assertion JWT
#         jwk_set = get_client_public_keys(claims['iss'])
#         return jwk.loads(jwk_set, header.get('kid'))

class _BearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):  
        print("_BearerTokenValidator->authenticate_token called..." + token_string)
        # oAuth2Token = OAuth2Token()
        # return oAuth2Token
        return oauth2Service.queryToken(token_string, 'access_token')



    def request_invalid(self, request):
        print("request_invalid?")
        return False

    def token_revoked(self, token):
        #print("token_revoked:" + str(token))
        return token.revoked

class _RevocationEndpoint(RevocationEndpoint):
    def query_token(self, token, token_type_hint, client):
        return oauth2Service.queryToken(token, token_type_hint) #, client)

    def revoke_token(self, token):
        token.revoked = True
        #db.session.add(token)  TODO
        #db.session.commit()

# class _IntrospectionEndpoint(IntrospectionEndpoint):
#     def query_token(self, token, token_type_hint, client):
#         return oauth2Service.queryToken(token, token_type_hint, client)

#     def introspect_token(self, token):
#         return {
#             'active': True,
#             'client_id': token.client_id,
#             'token_type': token.token_type,
#             'username': 'bob', #get_token_username(token),  TODO
#             'scope': token.get_scope(),
#             'sub': 'sub', #get_token_user_sub(token),  TODO
#             'aud': token.client_id,
#             'iss': 'https://server.example.com/',
#             'exp': token.expires_at,
#             'iat': token.issued_at,
#         }

print("Setting up oauth2 AuthorizationServer...")

OAUTH2_TOKEN_EXPIRES_IN = {
    'authorization_code': 864000,
    'implicit': 3600,
    'password': 864000,
    'client_credentials': 864000
}

authorizationServer = AuthorizationServer(
    query_client=oauth2Service.queryClient,
    save_token=oauth2Service.saveToken,
    **OAUTH2_TOKEN_EXPIRES_IN
)

# support all grants
#authorizationServer.register_grant(_AuthorizationCodeGrant)
authorizationServer.register_grant(_ImplicitGrant)
authorizationServer.register_grant(_PasswordGrant)
#authorizationServer.register_grant(_ClientCredentialsGrant)
#authorizationServer.register_grant(_RefreshTokenGrant)

# register grant to authorization server
# authorization.register_grant(JWTBearerGrant)

# support revocation
authorizationServer.register_endpoint(_RevocationEndpoint)
# authorizationServer.register_endpoint(_IntrospectionEndpoint)

# scopes definition
scopes = {
    'email': 'Access to your email address.',
    'connects': 'Access to your connected networks.',
    'profile': 'User Profile'
}

# protect resource
require_oauth = ResourceProtector()
require_oauth.register_token_validator(_BearerTokenValidator())

def init(app):
    print("initializing up AuthorizationServer...")
    authorizationServer.init_jwt_config(app)
    authorizationServer.init_app(app)
