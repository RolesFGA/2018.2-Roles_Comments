from rest_framework import permissions


"""    Custom permission to only allow owners of an object to edit it.    """
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """ Any user can read """
        if request.method in permissions.SAFE_METHODS:
            return True

        """ But only the author can edit """
        return obj.author == request.user
