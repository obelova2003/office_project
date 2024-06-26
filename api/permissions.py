from rest_framework import permissions

class ManagerRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'manager'
    

class ClientRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'client'
        
class CanSeeApplications(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.role == 'manager' or request.user.role == 'client' or request.user.role == 'director'