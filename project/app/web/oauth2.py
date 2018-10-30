from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.specs.rfc6749 import grants
from werkzeug.security import gen_salt
from project.app.models.user import User
from project.app.models.oauth2 import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token
from project.app.services import oauth2Service, userService
from project.app.services.utils import userUtils


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, user, request):
        return oauth2Service.addAuthorizationCode(client, user, request)

    def parse_authorization_code(self, code, client):
        return oauth2Service.parseAuthorizationCode(code, client)

    def delete_authorization_code(self, authorizationCode):
        oauth2Service.deleteAuthorizationCode(authorizationCode)

    def authenticate_user(self, authorizationCode):
        return oauth2Service.authenticateUser(authorizationCode)


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = userService.getUserByLogin(username)
        if(user is not None and userUtils.isUserValid(user, password)):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        item = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.isRefreshTokenExpired():
            return item

    def authenticate_user(self, credential):
        user = userService.getUserById(credential.user_id)
        return user

authorization = AuthorizationServer(
    query_client=oauth2Service.queryClientFunction,
    save_token=oauth2Service.saveTokenFunction,
)
require_oauth = ResourceProtector()


def configOauth(app):
    authorization.init_app(app)

    # support all grants
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(AuthorizationCodeGrant)
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)

    # support revocation
    authorization.register_endpoint(oauth2Service.revocationEndpoint)

    # protect resource
    require_oauth.register_token_validator(oauth2Service.bearerTokenValidator)
