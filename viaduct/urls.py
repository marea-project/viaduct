from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('api/', include('api.urls')),
	path('', include('search.urls')),
]
