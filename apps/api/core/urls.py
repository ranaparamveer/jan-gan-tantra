"""
URL configuration for Jan-Gan-Tantra API
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/wiki/', include('wiki.urls')),
    path('api/govgraph/', include('govgraph.urls')),
    path('api/issues/', include('issues.urls')),
    path('api/ai/', include('ai.urls')),
]
