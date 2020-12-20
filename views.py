
from rest_framework import viewsets
from .serializers import *
from .models import *

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class PerroViewSet(viewsets.ModelViewSet):
    queryset = Perro.objects.all()
    serializer_class = PerroSerializer

class GatoViewSet(viewsets.ModelViewSet):
    queryset = Gato.objects.all()
    serializer_class = GatoSerializer
