from App.views.dashboard import HomeView
from App.views.user_views import EditUser
from django.urls import path
from .views import *



urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("signup", CreateUser.as_view(), name='sign-up'),
    path("login", LoginUser.as_view(), name='log-in'),
    path("dashboard", DashboardView.as_view(), name='dashboard'),
    path("edit-user", EditUser.as_view(), name='edit-user'),
    path("delete-user", DeleteUser.as_view(), name='delete-user'),
    path("search-user/<int:pid>", SearchUserForInvite.as_view(), name='search-user'),
    
    path("new-project", CreateProject.as_view(), name='createproject'),
    path("project-settings/<int:pid>", ProjectSettings.as_view(), name='projectsettings'),
    path("delete-project/<int:pid>", ProjectDeleteView.as_view(), name='deleteproject'),
    path("project-actions/<int:pid>", ProjectActions.as_view(), name='projectactions'),

    path("sendNotif/<int:pid>", SendNotification.as_view(), name="sendnoti"),
    path("acceptInvite/", AcceptInvitation.as_view(), name="acceptinvite"),
    path("rejectInvite/", RejectInvitation.as_view(), name="acceptinvite"),


    path("tasks/<int:pid>", ShowTask.as_view(), name='showtasks'),
    path("create-task/<int:pid>", CreateTask.as_view(), name='createtask'),
    path("showcats/<int:pid>", ShowCategories.as_view()),


    path("manage-task/<int:pid>/<int:taskid>", ManageTask.as_view(), name='managetask'),
    path("showmanagers/<int:pid>/<int:taskid>", ShowManagers.as_view()),
    path("showusers/<int:pid>", ShowUsersToAssign.as_view()),

    path("showtasks/<int:pid>/<int:taskid>", ShowTasksForDependency.as_view()),
    path("addtaskDependency/<int:pid>/<int:taskid>", AddDependency.as_view()),
    path("removetaskDependency/<int:pid>/<int:taskid>", RemoveDependency.as_view()),

    path("feedback/<int:pid>/<int:taskid>", GiveFeedback.as_view()),
    path("submitTask/<int:pid>/<int:taskid>", SubmitTask.as_view()),
    path("endTask/<int:pid>/<int:taskid>", EndTask.as_view()),
    path("sendReminder/<int:pid>/<int:taskid>", SendReminder.as_view()),

]

