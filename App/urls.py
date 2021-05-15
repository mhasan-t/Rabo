from django.urls import path
from .views import CreateUser, LoginUser

urlpatterns = [
    path("signup", CreateUser.as_view(), name='sign-up'),
    path("login", LoginUser.as_view(), name='log-in')
]
