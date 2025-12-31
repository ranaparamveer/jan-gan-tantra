from django.urls import path
from .views import (
    IssueStatisticsView,
    DepartmentPerformanceView,
    TrendAnalysisView,
    DataExportView,
)

urlpatterns = [
    path('statistics/issues/', IssueStatisticsView.as_view(), name='public-issue-stats'),
    path('statistics/departments/', DepartmentPerformanceView.as_view(), name='public-dept-performance'),
    path('trends/', TrendAnalysisView.as_view(), name='public-trends'),
    path('export/', DataExportView.as_view(), name='public-export'),
]
