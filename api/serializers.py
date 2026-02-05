"""
Serializers for the api application.

Contains HyperlinkedModelSerializer implementations for exposed resources.
"""

from .models.user import User
from .models.arches import GraphModel
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for User model exposing url and username fields.

    Fields:
    - url: hyperlinked identity
    - username: Django username
    """
    class Meta:
        model = User
        fields = ['url', 'username']


class GraphModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for GraphModel objects exposing a small subset of fields.

    Fields:
    - url: hyperlinked identity
    - name: human readable name
    - description: short description text
    """
    class Meta:
        model = GraphModel
        fields = ['url', 'name', 'description']
