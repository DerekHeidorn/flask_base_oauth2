import time


from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.specs.rfc6749 import grants
from authlib.specs.rfc6750 import BearerTokenValidator
from project.app.services import oauth2Service, userService, commonService
from project.app.services.utils import userUtils
from project.app.web.utils import authUtils, serializeUtils


class _PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'none', 'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_user(self, username, password):
        user = userService.get_user_by_username(username)
        if user is not None:
            is_password_valid = userUtils.is_user_valid(user, password)
            if is_password_valid:
                return user

        return None


class _BearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        # oAuth2Token = OAuth2Token()
        # return oAuth2Token

        oauth2_secret_key = commonService.get_config_by_key('oauth2_secret_key')
        print("oauth2_secret_key=" + str(oauth2_secret_key))
        payload = authUtils.decode_auth_token_payload(token_string, oauth2_secret_key)
        print("payload=" + str(payload))
        if isinstance(payload, str):
            print(payload)
            return payload
        else:
            if isinstance(payload, dict) and 'jti' in payload:
                print("payload['jti']=" + str(payload['jti']))
                db_token = oauth2Service.query_token(payload['jti'], 'access_token')
                print("db_token=" + str(db_token))

                return db_token
        return None

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


def query_client(client_id):
    result = oauth2Service.query_client(client_id)

    return result


def save_token(token, request):

    oauth2_secret_key = commonService.get_config_by_key('oauth2_secret_key')
    decoded_token = authUtils.decode_auth_token_payload(token.get('access_token'), oauth2_secret_key)

    authorities = userUtils.get_user_authorities(request.user)
    authority_list = serializeUtils.serialize_authority(authorities)
    scope_list = ' '.join(authority_list)

    client_id = request.client.client_id
    user_id = request.user.get_user_id()
    token_type = token['token_type']
    scope = scope_list
    jti = decoded_token['jti']
    issued_at = time.time()
    expires_in = time.time() + token['expires_in']

    oauth2Service.save_token(client_id, user_id, token_type, scope, jti, issued_at, expires_in)


def generate_jwt_token(client, grant_type, user, scope):
    # print("client:" + str(client))
    # print("grant_type:" + str(grant_type))
    # print("user:" + str(user))
    # print("scope:" + str(scope))

    authorities = userUtils.get_user_authorities(user)
    oauth2_secret_key = commonService.get_config_by_key('oauth2_secret_key')
    print("(*)oauth2_secret_key:" + str(oauth2_secret_key))
    token = authUtils.encode_auth_token(user, authorities, oauth2_secret_key)
    # print("token:" + str(token ))
    print("token.decode('utf-8'):" + str(token))

    return token.decode("utf-8")

# ------------------------------------------------------------------------------
# Set up the Oauth Server
# ------------------------------------------------------------------------------


print("Creating AuthorizationServer...")
authorizationServer = AuthorizationServer(
    query_client=query_client,
    save_token=save_token
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
    app.config['OAUTH2_ACCESS_TOKEN_GENERATOR'] = generate_jwt_token

    print("initializing up AuthorizationServer...")
    authorizationServer.init_jwt_config(app)
    authorizationServer.init_app(app)
