from rest_framework.permissions import BasePermission


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type in [1, 2]


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 1


class IsSuperUserAssignedUserOrAdminOfAssignedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.user_type == 1:
            return True
        if obj.assigned_to == user:
            return True
        if (
            user.user_type == 2
            and getattr(obj.assigned_to, "assigned_admin", None) == user
        ):
            print("Admin has access to the task.")
            return True

        return False

    def has_delete_permission(self, request, view, obj):
        user = request.user
        if user.user_type in [1, 2]:
            return True
        return False
