
from rest_framework import serializers
from .models import *

class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = ExampleModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')

class EventModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = EventModel
        fields = ('id', 'time_event', 'title', 'description')
