from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Department, Designation, Officer, ContactVerification


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'parent', 'state', 'district', 'city']
    list_filter = ['level', 'state']
    search_fields = ['name', 'state', 'district', 'city']


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'level', 'typical_response_time']
    list_filter = ['department__level', 'level']
    search_fields = ['title', 'department__name']


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_active', 'verified_by_users', 'appointed_on']
    list_filter = ['is_active', 'designation__department__level']
    search_fields = ['name', 'designation__title', 'contact_email']
    readonly_fields = ['verified_by_users', 'last_verified_at', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(ContactVerification)
class ContactVerificationAdmin(admin.ModelAdmin):
    list_display = ['officer', 'verified_by', 'is_correct', 'verified_at']
    list_filter = ['is_correct', 'verified_at']
    readonly_fields = ['verified_at']
    date_hierarchy = 'verified_at'
