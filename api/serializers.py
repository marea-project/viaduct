from .models.user import User
from .models.arches import GraphModel
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'username']

class GraphModelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GraphModel
		fields = ['url', 'name', 'description']
