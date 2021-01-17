
from rest_framework import serializers
from .models import ExampleModel, DogModel

class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = ExampleModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')

class DogModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = DogModel
        fields = ('id', 'name', 'age', 'is_good_boy')
