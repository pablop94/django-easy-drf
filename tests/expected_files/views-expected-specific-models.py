
from rest_framework import viewsets
from .serializers import ExampleModelSerializer, DogModelSerializer
from .models import ExampleModel, DogModel

class ExampleModelViewSet(viewsets.ModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer

class DogModelViewSet(viewsets.ModelViewSet):
    queryset = DogModel.objects.all()
    serializer_class = DogModelSerializer
