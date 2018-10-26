import jwt
from datetime import datetime, timedelta

def encodeAuthToken(user, authorities):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        """
        iss (issuer), exp (expiration time), sub (subject), aud (audience)
        """
       
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'sau': authorities
        }
        return jwt.encode(
            payload,
            commonService.applicationConfigCache.get('oauth2_secret_key'),
            algorithm='HS256'
        )
    except Exception as e:
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