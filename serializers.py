
from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):

    class Meta():
        model = Event
        fields = ('id', 'title', 'description', 'event_picture')

class PerroSerializer(serializers.ModelSerializer):

    class Meta():
        model = Perro
        fields = ('id', 'totle', 'detalle', 'foto_pichicho')

class GatoSerializer(serializers.ModelSerializer):

    class Meta():
        model = Gato
        fields = ('id', 'title', 'description', 'event_picture')
