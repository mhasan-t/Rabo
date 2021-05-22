from App.views.user_views import EditUser
from django.urls import path
from .views import CreateUser, LoginUser, DashboardView, EditUser

urlpatterns = [
    path("signup", CreateUser.as_view(), name='sign-up'),
    path("login", LoginUser.as_view(), name='log-in'),
    path("dashboard", DashboardView.as_view(), name='dashboard'),
    path("edit-user", EditUser.as_view(), name='edit-user')
]
