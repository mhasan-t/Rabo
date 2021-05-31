from App.views.dashboard import HomeView
from App.views.user_views import EditUser
from django.urls import path
from .views import CreateUser, LoginUser, DashboardView, EditUser, DeleteUser, SearchUser



urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("signup", CreateUser.as_view(), name='sign-up'),
    path("login", LoginUser.as_view(), name='log-in'),
    path("dashboard", DashboardView.as_view(), name='dashboard'),
    path("edit-user", EditUser.as_view(), name='edit-user'),
    path("delete-user", DeleteUser.as_view(), name='delete-user'),
    path("search-user", SearchUser.as_view(), name='search-user'),
]

