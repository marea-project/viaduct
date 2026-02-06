"""
API view definitions.

Defines DRF viewsets that expose User and GraphModel resources.
"""

from .models.user import User
from .models.arches import ArchesInstance, GraphModel, Thesaurus
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, ArchesInstanceSerializer, GraphModelSerializer, ThesaurusSerializer, CompleteThesaurusSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
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

class ArchesInstanceViewSet(viewsets.ModelViewSet):
	queryset = ArchesInstance.objects.all()
	serializer_class = ArchesInstanceSerializer
	permission_classes = [permissions.IsAuthenticated]

class GraphModelViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = GraphModel.objects.all()
	serializer_class = GraphModelSerializer
	permission_classes = [permissions.IsAuthenticated]

class ThesaurusViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Thesaurus.objects.all()
	permission_classes = [permissions.IsAuthenticated]
	def get_serializer_class(self):
		if self.action == 'retrieve':
			return CompleteThesaurusSerializer
		return ThesaurusSerializer
