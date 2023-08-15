import jwt
from django.http import HttpResponseForbidden

from backend.models import WorkersMain
from config.settings import SECRET_KEY
from datetime import datetime, timedelta


def generate_jwt_token(user_id, user_name):
    payload = {
        'user_id': user_id,
        'user_name': user_name,
        'exp': datetime.utcnow() + timedelta(days=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def jwt_authentication_middleware(get_response):
    def middleware(request):
        authorization_header = request.headers.get('Authorization', '')
        if authorization_header.startswith('Login'):
            return get_response(request)
        if authorization_header.startswith('Bearer'):
            token = authorization_header.split(' ')[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                print(user_id)
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