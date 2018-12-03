import traceback
import jwt
import uuid
from datetime import datetime, timedelta
from app.web.utils import serializeUtils


def encode_auth_token(user, authorities, oauth2_secret_key):
    """
    Generates the Auth Token
    :param user:  User
    :param authorities:  User authorities
    :param oauth2_secret_key:
    :return: string
    """
    try:
        """
        iss (issuer), exp (expiration time), sub (subject), aud (audience)
        """
        authority_list = serializeUtils.serialize_authority(authorities)
       
        # make a random UUID
        jti_uuid = uuid.uuid4()

        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
            'iat': datetime.utcnow(),
            'sub': str(user.user_uuid),
            'jti': str(jti_uuid),
            'authorities': authority_list
        }
        jwt_encode = jwt.encode(
            payload,
            oauth2_secret_key,
            algorithm='HS512')

        return jwt_encode
        
    except Exception as e:
        print("Exception(2):" + str(e), str(e.with_traceback))
        traceback.print_exc()
        return e


def decode_auth_token(auth_token, oauth2_secret_key):
    """
    Decodes the auth token
    :param auth_token:
    :param oauth2_secret_key:
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
        payload = jwt.decode(auth_token,
                             key=oauth2_secret_key,
                             algorithms=['HS512'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def decode_auth_token_payload(jwt_token, oauth2_secret_key):
    """
    Decodes the auth token
    :param jwt_token:
    :param oauth2_secret_key:
    :return: payload as Dictionary
    """
    try:
        payload = jwt.decode(jwt_token,
                             key=oauth2_secret_key,
                             algorithms=['HS512'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
