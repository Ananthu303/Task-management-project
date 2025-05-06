from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["assigned_to"]

    def update(self, instance, validated_data):
        status_val = validated_data.get("status", instance.status)
        if status_val == "completed":
            errors = {}
            if "completion_report" not in validated_data:
                errors["completion_report"] = ["This field is required."]
            if "worked_hours" not in validated_data:
                errors["worked_hours"] = ["This field is required."]

            if errors:
                raise serializers.ValidationError(errors)

        return super().update(instance, validated_data)


class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["completion_report", "worked_hours"]

    def validate(self, data):
        task = self.instance
        if task.status != "completed":
            raise serializers.ValidationError(
                "Report is only available for completed tasks."
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    user_type_display = serializers.CharField(
        source="get_user_type_display", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password1",
            "password2",
            "user_type",
            "user_type_display",
            "assigned_admin",
        )

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
