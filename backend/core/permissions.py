from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Quyền chỉ cho phép chủ sở hữu tài nguyên được xem hoặc chỉnh sửa.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user
        return False