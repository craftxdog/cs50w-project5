"""
Serializers for Project APIs
"""

from rest_framework import serializers

from core.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name']
        read_only_fields = ['id']

class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for Project detail model"""
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['description']