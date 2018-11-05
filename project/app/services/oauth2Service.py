
from project.app.persist import oauth2Dao

from authlib.specs.rfc6749 import ClientMixin, OAuth2Request



class OAuth2Client(ClientMixin):

    # string of “public” or “confidential”
    client_type = None

    #  Validate if the client can handle the given grant_type. There are four grant types defined by RFC6749:
    # - authorization_code
    # - implicit
    # - client_credentials
    # - password
    grant_types = []

    allowed_redirect_uris = []

    scope = None

    # code and token
    response_types = []

    # client token_endpoint_auth_method defined via RFC7591: 
    #    none, client_secret_post, client_secret_basic
    token_endpoint_auth_method = None

    # client default redirect_uri.
    default_redirect_uri = None

    client_secret = None

    def __init__(self, client_id):
        self.client_id = client_id

    # Check client_secret matching with the client. For instance, in the client table, the column is called client_secret:
    def check_client_secret(self, client_secret):
        print("OAuth2Client->check_client_secret..."+ str(client_secret))
        return self.client_secret == client_secret

    # Validate if the client is the given client_type. The available choices are:
    def check_client_type(self, client_type):
        print("OAuth2Client->check_client_type..." + str(client_type))
        return self.client_type == client_type

    # Validate if the client can handle the given grant_type.
    def check_grant_type(self, grant_type):
        print("OAuth2Client->check_grant_type..." + str(grant_type))
        return grant_type in self.grant_types

    # Validate redirect_uri parameter in Authorization Endpoints.
    def check_redirect_uri(self, redirect_uri):
        print("OAuth2Client->check_redirect_uri..." + str(redirect_uri))
        return redirect_uri in self.allowed_redirect_uris

    # Validate if the request scopes are supported by this client.
    def check_requested_scopes(self, scopes):
        print("OAuth2Client->check_requested_scopes..." + str(scopes))
        return set(self.scope.split()).issuperset(scopes)

    # Validate if the client can handle the given response_type. There are two response types defined by RFC6749:
    def check_response_type(self, response_type):
        print("OAuth2Client->check_response_type..." + str(response_type))
        return response_type in self.response_types

    def check_token_endpoint_auth_method(self, method): 
        print("OAuth2Client->check_token_endpoint_auth_method..." + str(method))
        return self.token_endpoint_auth_method == method

    def get_default_redirect_uri(self):
        print("OAuth2Client->get_default_redirect_uri...")
        return self.default_redirect_uri

    # A method returns that if the client has client_secret value. 
    def has_client_secret(self):
        print("OAuth2Client->has_client_secret...")
        return bool(self.client_secret)



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

#                  client_id: CLTID-Zeq1LRso5q-iLU9RKCKnu
#              client_secret: t4lBxfkGiRHaByXbg9y5YEe084DZlHCYF7azLf1J
#                  issued_at: 1531271519
#                 expires_at: 0
#               redirect_uri: http://127.0.0.1:9000/oauth/token
# token_endpoint_auth_method: client_secret_basic
#                 grant_type: authorization_code password
#              response_type: code
#                      scope: profile
#                client_name: client_test
#                 client_uri: http://127.0.0.1:9000/
c1 = OAuth2Client('CLTID-Zeq1LRso5q-iLU9RKCKnu')
c1.client_name = 'client_test'
c1.client_type = 'public'
c1.client_secret = 't4lBxfkGiRHaByXbg9y5YEe084DZlHCYF7azLf1J'
c1.issued_at = 1531271519
c1.expires_at = 0
c1.allowed_redirect_uris = ['http://127.0.0.1:9000/oauth/token']
c1.token_endpoint_auth_method = 'none'
c1.grant_types = ['password']
c1.response_types = ['code']
c1.scope = 'profile'
c1.client_uri = 'http://127.0.0.1:9000/'

oAuth2Clients = [c1]

def queryClient(clientId):
    for c in oAuth2Clients:
        if c.client_id == clientId:
            return c
    return None

def queryToken(token, tokenTypeHint):
    print("oauth2Service->queryToken called...")
    return oauth2Dao.queryToken(token, tokenTypeHint)

def saveToken(clientId, userId, tokenType, scope, jti, issuedAt, expiresIn):
    return oauth2Dao.saveToken(clientId, userId, tokenType, scope, jti, issuedAt, expiresIn)
