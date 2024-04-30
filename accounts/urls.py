from django.urls import path
from .views import *

urlpatterns = [
    path('register/', AccountRegisterView.as_view(), name='register-account'),
    path('login/', AccountLoginView.as_view(), name='login-account'),
    path('logout/', AccountLogoutView.as_view(), name='logout-account'),
]