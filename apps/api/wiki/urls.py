from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SolutionViewSet, TemplateViewSet, SuccessPathViewSet, SolutionSuggestionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'solutions', SolutionViewSet)
router.register(r'templates', TemplateViewSet)
router.register(r'success-paths', SuccessPathViewSet)
router.register(r'suggestions', SolutionSuggestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
