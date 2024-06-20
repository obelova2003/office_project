from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()

router.register('users', views.OfficeUserViewSet, basename='users')

urlpatterns = router.urls