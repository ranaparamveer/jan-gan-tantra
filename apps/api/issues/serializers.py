from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Issue, IssueUpdate, IssueCluster


class IssueUpdateSerializer(serializers.ModelSerializer):
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True)
    
    class Meta:
        model = IssueUpdate
        fields = ['id', 'issue', 'message', 'updated_by_name', 'old_status', 
                  'new_status', 'created_at']
        read_only_fields = ['created_at']


class IssueListSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for map display"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Issue
        geo_field = 'location'
        fields = ['id', 'title', 'category_name', 'status', 'status_display', 
                  'created_at', 'upvotes', 'downvotes']


class IssueDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__('wiki.models', fromlist=['Category']).Category.objects.all(),
        source='category',
        write_only=True
    )
    reported_by_name = serializers.CharField(source='reported_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    updates = IssueUpdateSerializer(many=True, read_only=True)
    location_lat = serializers.SerializerMethodField()
    location_lng = serializers.SerializerMethodField()
    
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'category_name', 'category_id',
                  'location', 'location_lat', 'location_lng', 'address', 
                  'status', 'status_display', 'reported_by_name', 'assigned_to_name',
                  'evidence_photos', 'evidence_documents', 'created_at', 'updated_at',
                  'resolved_at', 'upvotes', 'downvotes', 'views', 'updates']
        read_only_fields = ['created_at', 'updated_at', 'resolved_at', 'upvotes', 'downvotes', 'views']
    
    def get_location_lat(self, obj):
        return obj.location.y if obj.location else None
    
    def get_location_lng(self, obj):
        return obj.location.x if obj.location else None


class IssueClusterSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for cluster visualization"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    petition_signature_count = serializers.SerializerMethodField()
    
    class Meta:
        model = IssueCluster
        geo_field = 'center_point'
        fields = ['id', 'category_name', 'issue_count', 'severity_score', 
                  'petition_text', 'petition_signature_count', 'detected_at', 'is_active']
    
    def get_petition_signature_count(self, obj):
        return obj.petition_signed_by.count()
