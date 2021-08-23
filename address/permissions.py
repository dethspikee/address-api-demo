from rest_framework import permissions


class OwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print("Calling object permissions!")
        return False
