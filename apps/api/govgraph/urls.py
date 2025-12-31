from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, DesignationViewSet, OfficerViewSet, ContactVerificationViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'designations', DesignationViewSet)
router.register(r'officers', OfficerViewSet)
router.register(r'verifications', ContactVerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
