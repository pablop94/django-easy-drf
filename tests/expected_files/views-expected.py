
from rest_framework import viewsets
from .serializers import ExampleModelSerializer, EventModelSerializer, DogModelSerializer
from .models import ExampleModel, EventModel, DogModel

class ExampleModelViewSet(viewsets.ModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer

class EventModelViewSet(viewsets.ModelViewSet):
    queryset = EventModel.objects.all()
    serializer_class = EventModelSerializer

class DogModelViewSet(viewsets.ModelViewSet):
    queryset = DogModel.objects.all()
    serializer_class = DogModelSerializer
