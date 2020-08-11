from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserRegisterView, UserInfoView


urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('', obtain_jwt_token),
    path('info/<int:pk>/', UserInfoView.as_view()),
]