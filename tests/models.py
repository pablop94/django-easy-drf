from django.db import models


class ExampleModel(models.Model):
    some_field = models.IntegerField()
    some_other_field = models.DecimalField(decimal_places=2, max_digits=10)
    third_field = models.DecimalField(decimal_places=2, max_digits=10)


class EventModel(models.Model):
    time_event = models.DateTimeField(verbose_name='Horario de evento')
    title = models.TextField(default='Titulo evento')
    description = models.TextField('Descripcion', blank=True, null=True)


class DogModel(models.Model):
    name = models.DateTimeField(verbose_name='Horario de evento')
    age = models.TextField(default='Titulo evento')
    is_good_boy = models.BooleanField()

