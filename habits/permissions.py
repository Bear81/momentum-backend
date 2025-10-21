from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Read allowed to anyone; write only for owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "owner", None)
        return owner == request.user
