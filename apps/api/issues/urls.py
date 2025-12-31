from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueViewSet, IssueClusterViewSet

router = DefaultRouter()
router.register(r'issues', IssueViewSet)
router.register(r'clusters', IssueClusterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
