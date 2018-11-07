import jwt
from jwt.exceptions import JWTDecodeError, JWTEncodeError
import uuid
from datetime import datetime, timedelta
from project.app.services import commonService
from project.app.web.utils import dtoUtils


def encode_auth_token(user, authorities):
    """
    Generates the Auth Token
    :param user:  User
    :param authorities:  User authorities
    :return: string
    """
    try:
        """
        iss (issuer), exp (expiration time), sub (subject), aud (audience)
        """
        authority_list = dtoUtils.authority_serialize(authorities)
       
        # make a random UUID
        jtiUuid = uuid.uuid4()

        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'jti': str(jtiUuid),
            'auth': authority_list
        }

        jwt_encode = jwt.JWT().encode(
                                      payload,
                                      commonService.application_config_cache.get('oauth2_secret_key'),
                                      alg='HS512'
                                      )

        return jwt_encode
        
    except JWTDecodeError as e:
        print("Exception(2):" + str(e), str(e.with_traceback))
        raise Exception(e)


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        # def decode(self,
        #            jwt,  # type: str
        #            key='',   # type: str
        #            verify=True,  # type: bool
        #            algorithms=None,  # type: List[str]
        #            options=None,  # type: Dict
        #            **kwargs):        
        payload = jwt.JWT().decode(auth_token,
                                   key=commonService.application_config_cache.get('oauth2_secret_key')
                                   )
        print("user:" + str(payload['sub']))
        return payload['sub']
    except JWTDecodeError:
        return 'Invalid token. Please log in again.'


def decode_auth_token_payload(jwt_token):
    """
    Decodes the auth token
    :param jwt_token:
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
        payload = jwt.JWT().decode(jwt_token,
                                   key=commonService.applicationConfigCache.get('oauth2_secret_key'))
        return payload
    except JWTDecodeError:
        return 'Invalid token. Please log in again.'