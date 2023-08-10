from backend.serializers import WorkersSerializer
from .models import WorkersMain


# TODO: add caching

from rest_framework import viewsets


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = WorkersMain.objects.all()
    serializer_class = WorkersSerializer

