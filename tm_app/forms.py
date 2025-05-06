from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import Task

User = get_user_model()


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "user_type"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "user_type": forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("Testpassword@123")
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
            cleaned_data["user"] = user
        return cleaned_data


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "completion_report",
            "worked_hours",
            "due_date",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        completion_report = cleaned_data.get("completion_report")
        worked_hours = cleaned_data.get("worked_hours")
        print(
            completion_report,
        )

        if status == "completed":
            if not completion_report:
                self.add_error(
                    "completion_report",
                    "This field is required if the task is completed.",
                )
            if worked_hours is None:
                self.add_error(
                    "worked_hours", "This field is required if the task is completed."
                )
