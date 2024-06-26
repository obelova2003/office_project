from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()

router.register('users', views.OfficeUserViewSet, basename='users')
router.register('auth', views.LoginViewSet, basename='auth')
router.register('logout', views.LogoutViewSet, basename='logout')

router.register('report', views.ReportViewSet, basename='report')
router.register('application', views.ApplicationViewSet, basename='application')

urlpatterns = router.urls
