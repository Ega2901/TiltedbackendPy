from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet, register_user

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register_user'),
]