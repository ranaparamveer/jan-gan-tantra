from django.urls import path
from .views import (
    TranslateView,
    DetectLanguageView,
    VoiceToTextView,
    SimplifyJargonView,
    DraftComplaintView,
    SummarizeDocumentView,
    GenerateRTIQueryView,
)
from .search_views import (
    SemanticSearchView,
    SimilarSolutionsView,
    IssueClustersView,
)

urlpatterns = [
    path('translate/', TranslateView.as_view(), name='translate'),
    path('detect-language/', DetectLanguageView.as_view(), name='detect-language'),
    path('voice-to-text/', VoiceToTextView.as_view(), name='voice-to-text'),
    path('simplify-jargon/', SimplifyJargonView.as_view(), name='simplify-jargon'),
    path('draft-complaint/', DraftComplaintView.as_view(), name='draft-complaint'),
    path('summarize-document/', SummarizeDocumentView.as_view(), name='summarize-document'),
    path('generate-rti/', GenerateRTIQueryView.as_view(), name='generate-rti'),
    
    # Semantic search
    path('search/', SemanticSearchView.as_view(), name='semantic-search'),
    path('similar-solutions/<int:solution_id>/', SimilarSolutionsView.as_view(), name='similar-solutions'),
    path('issue-clusters/', IssueClustersView.as_view(), name='issue-clusters'),
]
