"""
Tests for project api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project

from project.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
)

PROJECT_URL = reverse('project:project-list')

def detail_url(project_id):
    """Return project detail url"""
    return reverse('project:project-detail', args=[project_id])

def create_project(user, **params):
    """Create and return a new project"""
    defaults = {
        'project_name': 'test_project',
        'client_name': 'test_client_name',
        'description': 'test_project',
    }
    defaults.update(params)
    project = Project.objects.create(manager=user, **defaults)
    return project

class PublicProjectApiTests(TestCase):
    """Test unauthenticated API request"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving projects"""
        res = self.client.get(PROJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateProjectApiTests(TestCase):
    """Test authenticated API request"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            '<PASSWORD>',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_projects(self):
        """Test retrieving projects"""
        create_project(user=self.user)
        create_project(user=self.user)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_projects_list_limited_to_user(self):
        """Test retrieving projects for authenticated user"""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            '<PASSWORD>',
        )
        create_project(user=other_user)
        create_project(user=self.user)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.filter(manager=self.user)
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_project_detail(self):
        """Test retrieving project detail"""
        project = create_project(user=self.user)

        url = detail_url(project.id)
        res = self.client.get(url)

        serializer = ProjectDetailSerializer(project)
        self.assertEqual(res.data, serializer.data)

    def test_create_project(self):
        """Test creating project"""
        payload = {
            'project_name': 'test_project',
            'client_name': 'test_client_name',
        }
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(project, k), v)
        self.assertEqual(project.manager, self.user)