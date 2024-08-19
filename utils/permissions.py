from rest_framework import permissions

class IsEntityAdmin(permissions.BasePermission):
    """
    Custom permission to only allow entity admins to edit the entity.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admin of the entity.
        return obj.admin == request.user

class IsEntityCollaborator(permissions.BasePermission):
    """
    Custom permission to allow entity collaborators to edit certain aspects of the entity.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is a collaborator of the entity
        return request.user in obj.collaborators.all()

class IsEntityAdminOrCollaborator(permissions.BasePermission):
    """
    Custom permission to allow both entity admins and collaborators to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is either the admin or a collaborator
        return obj.admin == request.user or request.user in obj.collaborators.all()

class CanManageProducts(permissions.BasePermission):
    """
    Custom permission to allow entity admins and collaborators to manage products.
    """

    def has_permission(self, request, view):
        entity_id = view.kwargs.get('entity_id')
        if entity_id:
            from entities.models import Entity
            entity = Entity.objects.get(id=entity_id)
            return entity.admin == request.user or request.user in entity.collaborators.all()
        return False

class CanManageCollections(permissions.BasePermission):
    """
    Custom permission to allow entity admins and collaborators to manage collections.
    """

    def has_permission(self, request, view):
        entity_id = view.kwargs.get('entity_id')
        if entity_id:
            from entities.models import Entity
            entity = Entity.objects.get(id=entity_id)
            return entity.admin == request.user or request.user in entity.collaborators.all()
        return False

class CanPostContent(permissions.BasePermission):
    """
    Custom permission to allow entity admins and collaborators to post content.
    """

    def has_permission(self, request, view):
        entity_id = view.kwargs.get('entity_id')
        if entity_id:
            from entities.models import Entity
            entity = Entity.objects.get(id=entity_id)
            return entity.admin == request.user or request.user in entity.collaborators.all()
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user