from django.urls import path

from .views import home, results

urlpatterns = [
    path('', home),
    path('search', results)
]
