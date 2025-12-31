from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Issue, IssueUpdate, IssueCluster


@admin.register(Issue)
class IssueAdmin(GISModelAdmin):
    list_display = ['title', 'category', 'status', 'reported_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'address']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at', 'upvotes', 'views']
    date_hierarchy = 'created_at'
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 12,
        },
    }


@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'old_status', 'new_status', 'created_at']
    list_filter = ['old_status', 'new_status', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(IssueCluster)
class IssueClusterAdmin(GISModelAdmin):
    list_display = ['category', 'issue_count', 'severity_score', 'is_active', 'detected_at']
    list_filter = ['category', 'is_active', 'detected_at']
    readonly_fields = ['detected_at']
    date_hierarchy = 'detected_at'
