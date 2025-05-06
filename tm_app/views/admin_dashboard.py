from django.contrib.auth import get_user_model, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from tm_app.forms import CreateUserForm

from ..forms import LoginForm
from ..mixins import Admin_or_SuperAdminRequiredMixin, SuperAdminRequiredMixin

CustomUser = get_user_model()


class AdminPanelView(Admin_or_SuperAdminRequiredMixin, TemplateView):
    template_name = "admin/admin_dashboard.html"
    login_url = reverse_lazy("login-dashboard")


class CustomLoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        if user.user_type in [1, 2]:
            return redirect("admin_dashboard")
        else:
            return HttpResponse(f"Hello :{self.request.user.username}")


def logout_view(request):
    logout(request)
    return redirect(
        "login-dashboard"
    )

class CreateUserView(SuperAdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = CreateUserForm
    template_name = "admin/create_user.html"

    def get_success_url(self):
        user = self.object
        if user.user_type == CustomUser.UserType.ADMIN:
            return reverse_lazy("manage-admins")
        else:
            return reverse_lazy("manage-users")


class ManageUsersListView(Admin_or_SuperAdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "admin/manage_users.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = CustomUser.objects.exclude(
            Q(is_superuser=True) | Q(user_type=CustomUser.UserType.ADMIN)
        )

        if self.request.user.user_type == CustomUser.UserType.ADMIN:
            queryset = queryset.filter(assigned_admin=self.request.user)

        return queryset


class ManageAdminUsersListView(SuperAdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "admin/manage_admins.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.exclude(
            Q(is_superuser=True) | Q(user_type=CustomUser.UserType.USER)
        )


class UserUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username", "user_type", "assigned_admin"]
    template_name = "admin/update_user.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
        return form

    def get_success_url(self):
        user = self.object
        if user.user_type == CustomUser.UserType.ADMIN:
            return reverse_lazy("manage-admins")
        else:
            return reverse_lazy("manage-users")


class AdminUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username", "user_type"]
    template_name = "admin/update_admin.html"
    success_url = reverse_lazy("manage-admins")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
        return form

    def get_success_url(self):
        user = self.object
        if user.user_type == CustomUser.UserType.ADMIN:
            return reverse_lazy("manage-admins")
        else:
            return reverse_lazy("manage-users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_admin = self.object

        context["users"] = (
            CustomUser.objects.filter(user_type=CustomUser.UserType.USER)
            .filter(Q(assigned_admin__isnull=True) | Q(assigned_admin=current_admin))
            .order_by("username")
        )

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        CustomUser.objects.filter(assigned_admin=user).update(assigned_admin=None)

        if user.user_type == CustomUser.UserType.ADMIN:
            selected_user_ids = self.request.POST.getlist("assigned_users")
            if selected_user_ids:
                CustomUser.objects.filter(id__in=selected_user_ids).update(
                    assigned_admin=user
                )

        return response


class UserDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "admin/delete_user_confirm.html"

    def get_success_url(self):
        return reverse_lazy("manage-users")


class AdminDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "admin/delete_admin_confirm.html"

    def get_success_url(self):
        return reverse_lazy("manage-admins")
