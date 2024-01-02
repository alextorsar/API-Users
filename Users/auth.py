
from rest_framework.exceptions import AuthenticationFailed
import jwt

def authenticate(token):
    if not token:
            raise AuthenticationFailed('Not authenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Not authenticated')
    