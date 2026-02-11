"""
Test module for Viaduct's api app.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models.arches import ArchesInstance, GraphModel

class ApiEndpointTests(APITestCase):
    def setUp(self):
        # create a user that we will authenticate as
        self.user = User.objects.create_user(username='tester', password='testpass')
        # unauthenticated client
        self.anon = APIClient()
        # authenticated client
        self.client.force_authenticate(user=self.user)

        # prepare an ArchesInstance and a GraphModel for the models endpoint
        self.instance = ArchesInstance.objects.create(label='LocalArches', url='https://example.org/')
        # GraphModel requires slug and instance; create one directly in DB
        self.graph = GraphModel.objects.create(
            instance=self.instance,
            name='Test Model',
            description='A description',
            slug='test-model',
            config={}
        )

    # Root and router availability
    def test_api_root_available(self):
        """API root should be reachable (may show browsable links)."""
        resp = self.anon.get('/api/')
        # browsable root is usually accessible; allow 200 or 302 (redirects)
        self.assertIn(resp.status_code, (200, 302), f"Unexpected status for /api/: {resp.status_code}")

    # Users endpoint: unauthenticated access should be denied
    def test_users_list_requires_authentication(self):
        resp = self.anon.get('/api/users/')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    # GraphModel endpoint tests
    def test_models_list_requires_authentication(self):
        resp = self.anon.get('/api/models/')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_models_list_and_retrieve_authenticated(self):
        resp = self.client.get('/api/models/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # serializer exposes name and description
        data = resp.data.get('results', resp.data) if isinstance(resp.data, dict) else resp.data
        self.assertTrue(any(item.get('name') == 'Test Model' for item in data))

        # retrieve detail
        resp = self.client.get(f'/api/models/{self.graph.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('name'), 'Test Model')
        self.assertEqual(resp.data.get('description'), 'A description')

class PermissionEdgeCases(APITestCase):
    """Additional tests to ensure permission enforcement is consistent."""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pw')
        self.other = User.objects.create_user(username='bob', password='pw')
        self.client.force_authenticate(user=self.user)

    def test_user_cannot_access_without_auth(self):
        anon = APIClient()
        resp = anon.get('/api/users/')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
