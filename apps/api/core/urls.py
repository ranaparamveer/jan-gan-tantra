"""
URL configuration for Jan-Gan-Tantra API
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Jan-Gan-Tantra API",
        default_version='v1',
        description="Civic platform API for Indian citizens",
        terms_of_service="https://jan-gan-tantra.org/terms/",
        contact=openapi.Contact(email="api@jan-gan-tantra.org"),
        license=openapi.License(name="AGPL-3.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/wiki/', include('wiki.urls')),
    path('api/govgraph/', include('govgraph.urls')),
    path('api/issues/', include('issues.urls')),
    path('api/ai/', include('ai.urls')),
    
    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
