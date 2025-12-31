from django.contrib import admin
from .models import Solution, Category, Template, SuccessPath


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'language', 'success_rate', 'is_verified', 'created_at']
    list_filter = ['category', 'language', 'is_verified']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'template_type', 'category', 'language']
    list_filter = ['template_type', 'category', 'language']
    search_fields = ['title', 'content']


@admin.register(SuccessPath)
class SuccessPathAdmin(admin.ModelAdmin):
    list_display = ['solution', 'user', 'time_to_resolve', 'upvotes', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'upvotes']
    date_hierarchy = 'created_at'
