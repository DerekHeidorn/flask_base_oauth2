import jwt
import json
from datetime import datetime, timedelta
from services import commonService
from web.utils import publicJsonUtil

def encodeAuthToken(user, authorities):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        """
        iss (issuer), exp (expiration time), sub (subject), aud (audience)
        """
        authorityList = publicJsonUtil.authoritySerialize(authorities)
       
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'sau': json.dumps(authorityList)
        }
        jwt_encode = jwt.encode(
            payload,
            commonService.applicationConfigCache.get('oauth2_secret_key'),
            algorithm='HS256')

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
    try:
        payload = jwt.decode(authToken, commonService.applicationConfigCache.get('oauth2_secret_key'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'