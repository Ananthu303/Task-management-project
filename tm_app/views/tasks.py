from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from django.views.generic.edit import UpdateView

from tm_app.forms import TaskUpdateForm

from ..models import Task

CustomUser = get_user_model()
from ..mixins import Admin_or_SuperAdminRequiredMixin


class TaskCreateView(Admin_or_SuperAdminRequiredMixin, CreateView):
    model = Task
    fields = [
        "title",
        "description",
        "assigned_to",
        "due_date",
    ]
    template_name = "tasks/create_tasks.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field.widget, forms.DateInput):
                field.widget.input_type = "date"

        if self.request.user.user_type == CustomUser.UserType.ADMIN:
            form.fields["assigned_to"].queryset = CustomUser.objects.filter(
                assigned_admin=self.request.user
            )

        return form

    def get_success_url(self):
        return reverse_lazy("user-tasks", kwargs={"pk": self.object.assigned_to.id})


class AllTasksView(Admin_or_SuperAdminRequiredMixin, ListView):
    model = Task
    template_name = "tasks/all_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user

        if user.user_type == CustomUser.UserType.ADMIN:
            managed_users = CustomUser.objects.filter(assigned_admin=user)
            return Task.objects.filter(assigned_to__in=managed_users)

        elif user.user_type == CustomUser.UserType.USER:
            return Task.objects.filter(assigned_to=user)

        else:
            return Task.objects.all()


class UserTasksView(Admin_or_SuperAdminRequiredMixin, ListView):
    model = Task
    template_name = "tasks/user_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, id=self.kwargs["pk"])
        return Task.objects.filter(assigned_to=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context


class TaskUpdateView(Admin_or_SuperAdminRequiredMixin, UpdateView):
    model = Task

    form_class = TaskUpdateForm
    template_name = "tasks/edit_task.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field.widget, forms.DateInput):
                field.widget.input_type = "date"

        return form

    def get_success_url(self):
        return reverse_lazy("user-tasks", kwargs={"pk": self.object.assigned_to.id})


class TaskDeleteView(Admin_or_SuperAdminRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"

    def get_success_url(self):
        return reverse_lazy("user-tasks", kwargs={"pk": self.object.assigned_to.id})


class TaskReportView(Admin_or_SuperAdminRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_report.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        if user.user_type == CustomUser.UserType.ADMIN:
            managed_users = CustomUser.objects.filter(assigned_admin=user)
            return Task.objects.filter(
                status="completed", assigned_to__in=managed_users
            )
        return Task.objects.filter(status="completed")
