from django.conf.urls import  url
from django. urls import include, path
from . import views
from rest_framework import renderers
from rest_framework import routers
from .views import TransactionViewSet

router = routers.DefaultRouter()
router.register('', TransactionViewSet, basename='transactions')


urlpatterns = router.urls

urlpatterns += [
   path('quickbook', views.quickbook, name='quickbook'),
    path('callback', views.callback, name='callback'),
     path('qbo', views.fetchQboData, name='qbo'),
     path('xero', views.xero, name='xero'),
      path('xero_callback', views.xero_callback, name='xero_callback'),
      path('xeroData',views.fetchXeroData,name='xeroData')
]

