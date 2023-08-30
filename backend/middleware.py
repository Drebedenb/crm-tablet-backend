import jwt
from django.http import HttpResponseForbidden

from backend.models import WorkersMain
from config.settings import SECRET_KEY
from datetime import datetime, timedelta


def generate_jwt_token(expiration_in_days):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=expiration_in_days),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def jwt_authentication_middleware(get_response):
    def middleware(request):
        authorization_header = request.headers.get('Authorization', '')
        if request.path.endswith('/login'):
            return get_response(request)
        if authorization_header.startswith('Bearer'):
            token = authorization_header.split(' ')[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user = WorkersMain.objects.get(id=user_id)
                if not user:
                    return HttpResponseForbidden('There is no such user')
                # request.user = WorkersMain.objects.get(id=user_id)
            except jwt.ExpiredSignatureError:
                return HttpResponseForbidden('Token expired')
            except jwt.DecodeError:
                return HttpResponseForbidden('Token invalid')
        else:
            return HttpResponseForbidden("You are not authorized")
        return get_response(request)
    return middleware