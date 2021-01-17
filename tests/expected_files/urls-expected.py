
from rest_framework.routers import DefaultRouter
from .views import ExampleModelViewSet, EventModelViewSet, DogModelViewSet
router = DefaultRouter()
router.register('example-model', ExampleModelViewSet, basename='example-model')
router.register('event-model', EventModelViewSet, basename='event-model')
router.register('dog-model', DogModelViewSet, basename='dog-model')
urlpatterns = router.urls
