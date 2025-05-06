from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class UserType(models.IntegerChoices):
        SUPERADMIN = 1, "SuperAdmin"
        ADMIN = 2, "Admin"
        USER = 3, "User"

    user_type = models.PositiveSmallIntegerField(
        choices=UserType.choices, default=UserType.USER
    )
    assigned_admin = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"user_type": UserType.ADMIN},
        related_name="assigned_users",
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": CustomUser.UserType.USER},
        related_name="tasks",
    )
    due_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.assigned_to.username})"
