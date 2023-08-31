import jwt
from django.db.models import Q
from django.http import HttpResponseForbidden
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from backend.serializers import WorkersSerializer, OrdersSerializer
from config.settings import SECRET_KEY
from .middleware import generate_jwt_token
from .models import WorkersMain, OrdersMain
from rest_framework.response import Response
from rest_framework import exceptions, viewsets
from datetime import datetime, timedelta


class OrdersList(ListAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self):
        authorization_header = self.request.headers.get('Authorization', '')
        if authorization_header.startswith('Bearer'):
            token = authorization_header.split(' ')[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user = WorkersMain.objects.get(id=user_id)
                if not user:
                    return HttpResponseForbidden('There is no such user')
            except jwt.ExpiredSignatureError:
                return HttpResponseForbidden('Token expired')
            except jwt.DecodeError:
                return HttpResponseForbidden('Token invalid')
        else:
            return HttpResponseForbidden("You are not authorized")
        if user.RoleManager == '1' and user.workersuseraccess_set.filter(key='ManagerVisibleAll').values()[0]['value'] == '1':
            # If RoleManager is 1 and ManagerVisibleAll is 1, return all orders
            queryset = OrdersMain.objects.filter(OrderStatus__in=[1, 2, 3, 4])
        else:
            # If not, filter orders based on the worker's orders
            queryset = OrdersMain.objects.filter(
                Q(OrderStatus__in=[1, 2, 3, 4]) &   # TODO: make it more intellectual without hardcode
                Q(OrderManager=user.id)
            )
        return queryset


class AuthenticateUser(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            raise exceptions.AuthenticationFailed(('No credentials provided.'))
        user = WorkersMain.objects.get(UserLogin=username, UserPassword=password)
        if user is None:
            raise exceptions.AuthenticationFailed(('Invalid username/password.'))
        expiration_in_days = 1
        token_jwt = generate_jwt_token(user.id, expiration_in_days)
        response = {
            'username': user.ShortName,
            'accessToken': token_jwt,
            'expiredAt': datetime.utcnow() + timedelta(days=expiration_in_days),
        }
        return Response(response)

