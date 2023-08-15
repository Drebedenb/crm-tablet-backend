from rest_framework.views import APIView
from backend.serializers import WorkersSerializer
from .middleware import generate_jwt_token
from .models import WorkersMain
from rest_framework.response import Response
from rest_framework import exceptions, viewsets


# TODO: add caching


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = WorkersMain.objects.all()
    serializer_class = WorkersSerializer


class AuthenticateUser(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            raise exceptions.AuthenticationFailed(('No credentials provided.'))

        user = WorkersMain.objects.get(UserLogin=username, UserPassword=password)
        if user is None:
            raise exceptions.AuthenticationFailed(('Invalid username/password.'))

        token_jwt = generate_jwt_token(user.id, user.ShortName)
        return Response(token_jwt)

