"""
Views for project app.
"""

from rest_framework import viewsets
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Project
from project import serializers

class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for Project app."""
    serializer_class = serializers.ProjectDetailSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the projects belonging to the authenticated user."""
        return self.queryset.filter(manager=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return serializers.ProjectSerializer

        return self.serializer_class

    def preform_create(self, serializer):
        """Create a new project."""
        serializer.save(manager=self.request.user)