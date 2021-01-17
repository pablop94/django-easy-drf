# django-easy-drf

A package that makes for you the repetitive work of creating Serializers, ViewSets and URLs for django rest framework.

## Installation
On a virtualenv run:
```
pip install django-easy-drf
```

## Usage
On the same virtualenv, you will have *easy-drf* command available, so run:
```
easy-drf
```
This command will create serializers.py, views.py and urls.py files on the same directory, with all the classes created.

Note: requires that a file called models.py exists on the current directory.

Suppose you have a models.py file with the following content:
```python
from django.db import models

class ExampleModel(models.Model):
    some_field = models.IntegerField()
    some_other_field = models.DecimalField(decimal_places=2, max_digits=10)
    third_field = models.DecimalField(decimal_places=2, max_digits=10)
```

The resulting serializers.py will be like this:
```python
from rest_framework import serializers
from .models import ExampleModel

class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = ExampleModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')
```

The resulting views.py will be like this:
```python
from rest_framework import viewsets
from .serializers import ExampleModelSerializer
from .models import ExampleModel

class ExampleModelViewSet(viewsets.ModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer
```

The resulting urls.py will be like this:
```python
from rest_framework.routers import DefaultRouter
from .views import ExampleModelViewSet
router = DefaultRouter()
router.register('example-model', ExampleModelViewSet, basename='example-model')
urlpatterns = router.urls
```

#### Forcing creation
If you want to avoid command prompt, you can force it:
```
easy-drf --force
```
or less verbose:
```
easy-drf -f
```
#### Creating only one file
Sometimes you don't need all files (views, serializers and urls) so you can specify which ones should be created. Options are:
- 's' for serializers.py
- 'v' for views.py
- 'u' for urls.py

For example, this command will create serializers.py and views.py
```
easy-drf --files s v
```
If you don't specify --files argument, all files will be created.


#### Creating only one model
Sometimes you don't need all models, so you can specify which ones should be created. 

Suppose you have a models.py file with the following content:
```python
from django.db import models

class ExampleModel(models.Model):
    some_field = models.IntegerField()
    some_other_field = models.DecimalField(decimal_places=2, max_digits=10)
    third_field = models.DecimalField(decimal_places=2, max_digits=10)


class DogModel(models.Model):
    name = models.DateTimeField(verbose_name='Horario de evento')
    age = models.TextField(default='Titulo evento')
    is_good_boy = models.BooleanField()
```

But you know that *only DogModel will be serialized*, so you can create a serializer only for this model, running:
```
easy-drf --files s -m DogModel
```

The resulting serializers.py file will be like this:
```python
from rest_framework import serializers
from .models import DogModel

class DogModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = DogModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')
```

You can use -m or --models and specify some models:
```
easy-drf --files s --models DogModel ExampleModel
```

##### Append by default
If any of the named files exist on the current directory, the result will be appended to their content.
Suppose you have a models.py file with the following content:
```python
from django.db import models

class ExampleModel(models.Model):
    some_field = models.IntegerField()
    some_other_field = models.DecimalField(decimal_places=2, max_digits=10)
    third_field = models.DecimalField(decimal_places=2, max_digits=10)

class DogModel(models.Model):
    name = models.DateTimeField(verbose_name='Horario de evento')
    age = models.TextField(default='Titulo evento')
    is_good_boy = models.BooleanField()
```

And you have a serializers.py file like this:
```python
from rest_framework import serializers
from .models import ExampleModel

class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = ExampleModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')
```

Then you run 
```
easy-drf -m DogModel --files s
```

The resulting serializers.py file will be like this:
```python
from rest_framework import serializers
from .models import ExampleModel, DogModel

class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = ExampleModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')

class DogModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = DogModel
        fields = ('id', 'some_field', 'some_other_field', 'third_field')
```
The effect of the command was:
- In the second line of the serializers.py file, DogModel was added as an import.
- DogModelSerializer is created at the bottom of the file, keeping the original file's content

*This is the default behavior, but an option to rewrite the entire file will be added soon.*

#### Getting help
For help, type:
```
easy-drf --help
```
or less verbose:
```
easy-drf -h
```
This command will list the available cli options.

#### Future developments
- [x] Warn users about files override.
- [x] Allow users to force script without prompt.
- [x] Allow users to create just one specific file.
- [x] Allow users to create just one model.
- [ ] Allow users to override default append behavior.
- [ ] Allow users to specify different models file.
- [ ] Allow users to specify different results file names.


### Contributing
If you have an idea or an implementation, let me know by submitting an issue or a PR.
