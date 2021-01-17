
from rest_framework import viewsets
from .serializers import ExampleModelSerializer, DogModelSerializer, EventModelSerializer
from .models import ExampleModel, DogModel, EventModel

class ExampleModelViewSet(viewsets.ModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer

class DogModelViewSet(viewsets.ModelViewSet):
    queryset = DogModel.objects.all()
    serializer_class = DogModelSerializer

class EventModelViewSet(viewsets.ModelViewSet):
    queryset = EventModel.objects.all()
    serializer_class = EventModelSerializer