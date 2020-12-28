
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('example-model', ExampleModelViewSet, basename='example-model')
router.register('event-model', EventModelViewSet, basename='event-model')
urlpatterns = router.urls
