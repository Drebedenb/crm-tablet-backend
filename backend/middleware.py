import jwt
from django.http import HttpResponseForbidden

from backend.models import WorkersMain
from config.settings import SECRET_KEY
from datetime import datetime, timedelta


def generate_jwt_token(user_id, expiration_in_days):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=expiration_in_days),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

