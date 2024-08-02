from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import *

urlpatterns = [
    path('users/by_telegram_id/<str:telegram_id>/', views.UserDetail.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('tasks/', UserTasks.as_view()),
    path('tasks/<int:task_id>/complete/', CompleteTask.as_view()),
    path('tasks/create/', CreateGlobalTask.as_view()),
    path('users/<str:telegram_id>/start_farming/', views.StartFarming.as_view()),
    path('users/<str:telegram_id>/claim_rewards/', views.ClaimRewards.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
