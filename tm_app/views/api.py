from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied

from ..mixins import NoAuthMixin
from ..models import Task
from ..permissions import IsSuperUserAssignedUserOrAdminOfAssignedUser
from ..serializers import (
    LoginSerializer,
    TaskReportSerializer,
    TaskSerializer,
    TokenSerializer,
    UserSerializer,
)


CustomUser = get_user_model()


class RegisterView(NoAuthMixin, GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.save()
        user = validated_data
        return Response(
            {
                "message": "User registered successfully",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(NoAuthMixin, GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid username or password.")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        token_data = TokenSerializer({"refresh": str(refresh), "access": access_token})

        return Response(token_data.data, status=status.HTTP_200_OK)




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs.get("pk"))
        self.check_object_permissions(self.request, obj)
        return obj


    def get_queryset(self):
        if self.action in ["list", "retrieve", "update"]:
            return Task.objects.filter(assigned_to=self.request.user)
        return Task.objects.all()

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        permission = IsSuperUserAssignedUserOrAdminOfAssignedUser()
        if not permission.has_delete_permission(request, self, obj):
            raise PermissionDenied("You do not have permission to delete this task.")

        self.perform_destroy(obj)
        return Response(
            {"detail": "Task deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="report",
        permission_classes=[IsAuthenticated, IsSuperUserAssignedUserOrAdminOfAssignedUser],
    )
    def report(self, request, pk=None):
        task = self.get_object()
        serializer = TaskReportSerializer(task)
        return Response(serializer.data)
