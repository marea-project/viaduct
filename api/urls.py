from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, GraphModelViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"models", GraphModelViewSet)

urlpatterns = [
	path("", include(router.urls)),
]
