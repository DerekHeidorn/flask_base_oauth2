
import time
from datetime import datetime
from cacheout import Cache

from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.specs.rfc6749 import grants
from authlib.specs.rfc6750 import BearerTokenValidator
from authlib.specs.rfc6749.errors import AccessDeniedError
from authlib.specs.rfc6749 import TokenMixin

from app import core
from app.persist import baseDao, userDao
from app.services import oauth2Service, userService
from app.services.utils import userUtils
from app.web.utils import authUtils


_authorization_server = None
_token_cache = Cache(maxsize=1000, ttl=5 * 60)


class _OAuth2TokenMixin(TokenMixin):
    user = None
    scope = None
    expires_in = None
    expires_at = None

    def get_scope(self):
        """A method to get scope of the authorization code. For instance,
        the column is called ``scope``::

            def get_scope(self):
                return self.scope

        :return: scope string
        """
        return self.scope

    def get_expires_in(self):
        """A method to get the ``expires_in`` value of the token. e.g.
        the column is called ``expires_in``::

            def get_expires_in(self):
                return self.expires_in

        :return: timestamp int
        """
        return self.expires_in

    def get_expires_at(self):
        """A method to get the value when this token will be expired. e.g.
        it would be::

            def get_expires_at(self):
                return self.created_at + self.expires_in

        :return: timestamp int
        """
        return self.expires_at


class _PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'none'  # , 'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_user(self, username_or_alias, password):
        session = baseDao.get_session()

        user = userDao.get_user_by_username(username_or_alias, session)

        # Optional login using the alias
        # if user is None:  # no username found, try Alias
        #     user = userDao.get_user_by_alias(username_or_alias, session)

        core.logger.debug("authenticate_user: " + username_or_alias + ", user_object: " + str(user))

        if user is not None:

            if user.is_active:

                is_password_valid = userUtils.is_user_valid(user, password)
                if is_password_valid:
                    user.last_attempts_ts = datetime.now()
                    userDao.update_user(user, session)
                    return user
                else:
                    user.failed_attempt_count += 1
                    user.last_attempts_ts = datetime.now()
                    userDao.update_user(user, session)

                    if user.failed_attempt_count > 8:
                        userService.deactivate_account(user.user_id)

                    core.logger.debug("raising AccessDeniedError: 'Password is invalid'")
                    raise AccessDeniedError('Password is invalid')
            else:
                core.logger.debug("raising AccessDeniedError: 'User is not active'")
                raise AccessDeniedError('User is not active')
        else:
            core.logger.debug("raising AccessDeniedError: 'User does not exist'")
            raise AccessDeniedError('User does not exist')


class _BearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        # oAuth2Token = OAuth2Token()
        # return oAuth2Token

        oauth2_secret_key = core.global_config["APP_JWT_KEY"]
        # print("oauth2_secret_key=" + str(oauth2_secret_key))
        payload = authUtils.decode_auth_token_payload(token_string, oauth2_secret_key)
        print("payload=" + str(payload))
        if isinstance(payload, dict):
            user = userService.get_user_by_uuid(payload['sub'])

            if user is None:
                raise AccessDeniedError("No active user")

            token = _OAuth2TokenMixin()
            token.user = user
            token.scope = payload['authorities']
            token.expires_in = payload['exp'] - payload['iat']
            token.expires_at = payload['exp']

            return token
        else:
            if isinstance(payload, dict) and 'jti' in payload:
                jti_key = payload['jti']
                if _token_cache.has(jti_key):
                    print("got cached token: " + jti_key)
                    token = _token_cache.get(jti_key)
                    return token

                # print("payload['jti']=" + str(payload['jti']))
                db_token = oauth2Service.query_token(jti_key, 'access_token')
                print("caching token: " + jti_key)
                _token_cache.add(jti_key, db_token)
                return db_token
        return None

    def request_invalid(self, request):
        print("request_invalid->request:" + str(request))
        return False

    def token_revoked(self, token):
        print("token_revoked:" + str(token))
        return False


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

    oauth2_secret_key = core.global_config["APP_JWT_KEY"]
    decoded_token = authUtils.decode_auth_token_payload(token.get('access_token'), oauth2_secret_key)

    # authorities = userUtils.get_user_authorities(request.user)
    # authority_list = serializeUtils.serialize_authority(authorities)
    # scope_list = ' '.join(authority_list)
    scope_list = 'app.public'

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
    oauth2_secret_key = core.global_config["APP_JWT_KEY"]
    print("(*)oauth2_secret_key:" + str(oauth2_secret_key))
    token = authUtils.encode_auth_token(user, authorities, oauth2_secret_key)
    # print("token:" + str(token ))
    print("token.decode('utf-8'):" + str(token))

    return token.decode("utf-8")

# ------------------------------------------------------------------------------
# Set up the Oauth Server
# ------------------------------------------------------------------------------


# protect resource
require_oauth = ResourceProtector()
require_oauth.register_token_validator(_BearerTokenValidator())


def create_token_response():
    if _authorization_server is None:
        raise Exception("authorization_server has not been started correctly.")

    return _authorization_server.create_token_response()


def init(app):
    app.config['OAUTH2_ACCESS_TOKEN_GENERATOR'] = generate_jwt_token

    print("initializing up AuthorizationServer...")
    global _authorization_server
    _authorization_server = AuthorizationServer(
        query_client=query_client,
        save_token=save_token
    )

    # supported grants
    _authorization_server.register_grant(_PasswordGrant)

    _authorization_server.init_jwt_config(app)
    _authorization_server.init_app(app)
