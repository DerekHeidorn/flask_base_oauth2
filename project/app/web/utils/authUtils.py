import jwt
import json
import uuid
from datetime import datetime, timedelta
from project.app.services import commonService
from project.app.services.utils import userUtils
from project.app.web.utils import dtoUtils



def encodeAuthToken(user, authorities):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        """
        iss (issuer), exp (expiration time), sub (subject), aud (audience)
        """
        authorityList = dtoUtils.authoritySerialize(authorities)
       
        # make a random UUID
        jtiUuid = uuid.uuid4()

        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'jti': str(jtiUuid),
            'auth': authorityList
        }
        jwt_encode = jwt.encode(
            payload,
            commonService.applicationConfigCache.get('oauth2_secret_key'),
            algorithm='HS512')

        return jwt_encode
        
    except Exception as e:
        print("Exception(2):" + str(e), str(e.with_traceback))
        return e

def decodeAuthToken(authToken):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    print("decodeAuthToken->authToken:" + str(authToken))
    try:
        # def decode(self,
        #            jwt,  # type: str
        #            key='',   # type: str
        #            verify=True,  # type: bool
        #            algorithms=None,  # type: List[str]
        #            options=None,  # type: Dict
        #            **kwargs):        
        payload = jwt.decode(authToken, 
                                key=commonService.applicationConfigCache.get('oauth2_secret_key'),
                                algorithms=['HS512'])
        print("user:" + str(payload['sub']))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def decodeAuthTokenPayload(jwtToken):
    """
    Decodes the auth token
    :param authToken:
    :return: payload as Dictionary
    """
    try:
        # def decode(self,
        #            jwt,  # type: str
        #            key='',   # type: str
        #            verify=True,  # type: bool
        #            algorithms=None,  # type: List[str]
        #            options=None,  # type: Dict
        #            **kwargs): 
        print("decodeAuthToken->jwtToken:" + str(jwtToken))       
        payload = jwt.decode(jwtToken, 
                                key=commonService.applicationConfigCache.get('oauth2_secret_key'))
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'