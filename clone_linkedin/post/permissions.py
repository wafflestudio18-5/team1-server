from rest_framework.permissions import BasePermission

class IsOwnerOrReadOrCreate(BasePermission):
    SAFE_METHODS = ('GET', 'POST')
    message = 'The user is not the owner of the object'

    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS:
            return True
        return obj.user == request.user
