from .models.user import User
from .models.arches import GraphModel
from rest_framework import permissions, viewsets

from .serializers import UserSerializer, GraphModelSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by("-date_joined")
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

class GraphModelViewSet(viewsets.ModelViewSet):
	queryset = GraphModel.objects.all()
	serializer_class = GraphModelSerializer
	permission_classes = [permissions.IsAuthenticated]
