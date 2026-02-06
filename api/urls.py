"""
URL routing for the api application.

This module registers DRF viewsets into a DefaultRouter and exposes the router
URLs at the package root.
"""

from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, ArchesInstanceViewSet, GraphModelViewSet, ThesaurusViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"instances", ArchesInstanceViewSet)
router.register(r"models", GraphModelViewSet)
router.register(r"thesauri", ThesaurusViewSet)

urlpatterns = [
	path("", include(router.urls)),
]
