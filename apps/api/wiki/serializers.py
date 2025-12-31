from rest_framework import serializers
from .models import Solution, Category, Template, SuccessPath


class CategorySerializer(serializers.ModelSerializer):
    solution_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'solution_count']
    
    def get_solution_count(self, obj):
        return obj.solutions.count()


class TemplateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Template
        fields = ['id', 'title', 'template_type', 'content', 'language', 'category', 'category_name']


class SuccessPathSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = SuccessPath
        fields = ['id', 'solution', 'user_name', 'steps_taken', 'outcome', 
                  'time_to_resolve', 'evidence_urls', 'created_at', 'upvotes']
        read_only_fields = ['created_at', 'upvotes']


class SolutionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Solution
        fields = ['id', 'title', 'description', 'category_name', 'language', 
                  'success_rate', 'is_verified', 'created_at']


class SolutionDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested data"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
    )
    success_paths = SuccessPathSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Solution
        fields = ['id', 'title', 'description', 'problem_keywords', 'steps', 
                  'success_rate', 'language', 'category', 'category_id', 
                  'created_by_name', 'created_at', 'updated_at', 'is_verified',
                  'success_paths']
        read_only_fields = ['created_at', 'updated_at', 'success_rate']
