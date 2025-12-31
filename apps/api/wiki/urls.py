from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SolutionViewSet, TemplateViewSet, SuccessPathViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'solutions', SolutionViewSet)
router.register(r'templates', TemplateViewSet)
router.register(r'success-paths', SuccessPathViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
