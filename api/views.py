"""
API view definitions.

Defines DRF viewsets that expose User and GraphModel resources.
"""

from .models.user import User
from .models.arches import GraphModel
from rest_framework import permissions, viewsets

from .serializers import UserSerializer, GraphModelSerializer

class UserViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for listing and managing users.

	- queryset: returns all users ordered by date_joined descending.
	- serializer_class: UserSerializer
	- permission_classes: requires authentication

	Example::

		GET /api/users/  -> list users (authenticated)
	"""
	queryset = User.objects.all().order_by("-date_joined")
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

class GraphModelViewSet(viewsets.ModelViewSet):
	queryset = GraphModel.objects.all()
	serializer_class = GraphModelSerializer
	permission_classes = [permissions.IsAuthenticated]
