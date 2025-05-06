from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

CustomUser = get_user_model()
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden


class JWTAuthMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class NoAuthMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]


class AllowAnyForCreateMixin:
    def get_permissions(self):
        if getattr(self, "action", None) == "create":
            return [AllowAny()]
        return super().get_permissions()


class AllowAnyForListMixin:
    def get_permissions(self):
        if getattr(self, "action", None) == "list":
            return [AllowAny()]
        return super().get_permissions()


class SuperAdminRequiredMixin(LoginRequiredMixin, AccessMixin):
    """Allow only SuperAdmin users to access the view."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != CustomUser.UserType.SUPERADMIN:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(request, *args, **kwargs)


class Admin_or_SuperAdminRequiredMixin(LoginRequiredMixin, AccessMixin):
    """Allow only SuperAdmin users to access the view."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type not in {
            CustomUser.UserType.SUPERADMIN,
            CustomUser.UserType.ADMIN,
        }:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(request, *args, **kwargs)
