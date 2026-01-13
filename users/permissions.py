from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == view.get_object().owner

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
