from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from tm_app.views.admin_dashboard import (AdminDeleteView, AdminPanelView,
                                AdminUpdateView, CreateUserView,
                                CustomLoginView, ManageAdminUsersListView,
                                ManageUsersListView, UserDeleteView,
                                UserUpdateView, logout_view)
from tm_app.views.api import LoginView, RegisterView, TaskViewSet
from tm_app.views.tasks import (AllTasksView, TaskCreateView, TaskDeleteView,
                                TaskReportView, TaskUpdateView, UserTasksView)

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    #AUTH
    path("", CustomLoginView.as_view(), name="login-dashboard"),
    path("logout/", logout_view, name="logout"),
    #USERS-MANAGEMENT
    path("admin-dashboard/", AdminPanelView.as_view(), name="admin_dashboard"),
    path("manage-users/", ManageUsersListView.as_view(), name="manage-users"),
    path("manage-admins/", ManageAdminUsersListView.as_view(), name="manage-admins"),
    path("create-users/", CreateUserView.as_view(), name="create-users"),
    path("update-user/<int:pk>/", UserUpdateView.as_view(), name="update-user"),
    path("update-admin/<int:pk>/", AdminUpdateView.as_view(), name="update-admin"),
    path("delete-user/<int:pk>/", UserDeleteView.as_view(), name="delete-user"),
    path("delete-admin/<int:pk>/", AdminDeleteView.as_view(), name="delete-admin"),
    #TASKS MANAGEMENT
    path("create-tasks/", TaskCreateView.as_view(), name="create-tasks"),
    path("all-tasks/", AllTasksView.as_view(), name="all-tasks"),
    path("user-tasks/<int:pk>/", UserTasksView.as_view(), name="user-tasks"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="edit-task"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="delete-task"),
    path("task-report/", TaskReportView.as_view(), name="task-report"),
    # APIS
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
