from django.urls import path,include
from . import views
from rest_framework import routers
from .views import AuthViewSet
from rest_framework import renderers



router = routers.DefaultRouter()
router.register('', AuthViewSet, basename='auth')


urlpatterns = router.urls