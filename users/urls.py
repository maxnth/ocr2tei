from django.urls import path

from users import views

urlpatterns = [
    path('user_info/', views.UserInfo.as_view(), name='user_info'),
    path('accounts/signup/', views.SignUp.as_view(), name='user_signup'),
]
