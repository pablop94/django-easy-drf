
from rest_framework.routers import DefaultRouter
from .views import ExampleModelViewSet, DogModelViewSet
router = DefaultRouter()
router.register('example-model', ExampleModelViewSet, basename='example-model')
router.register('dog-model', DogModelViewSet, basename='dog-model')
urlpatterns = router.urls
