from rest_framework import serializers
from .models import Department, Designation, Officer, ContactVerification


class DepartmentSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    designation_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'level', 'level_display', 'parent', 'parent_name',
                  'state', 'district', 'city', 'ward_number', 'designation_count']
    
    def get_designation_count(self, obj):
        return obj.designations.count()


class DesignationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    current_officer = serializers.SerializerMethodField()
    
    class Meta:
        model = Designation
        fields = ['id', 'title', 'department', 'department_name', 'level', 
                  'responsibilities', 'typical_response_time', 'current_officer']
    
    def get_current_officer(self, obj):
        officer = obj.officers.filter(is_active=True).first()
        if officer:
            return OfficerSerializer(officer).data
        return None


class OfficerSerializer(serializers.ModelSerializer):
    designation_title = serializers.CharField(source='designation.title', read_only=True)
    department_name = serializers.CharField(source='designation.department.name', read_only=True)
    escalation_level = serializers.IntegerField(source='designation.level', read_only=True)
    
    class Meta:
        model = Officer
        fields = ['id', 'designation', 'designation_title', 'department_name', 
                  'escalation_level', 'name', 'contact_email', 'contact_phone', 
                  'office_address', 'verified_by_users', 'last_verified_at',
                  'appointed_on', 'tenure_ends_on', 'is_active', 'created_at']
        read_only_fields = ['verified_by_users', 'last_verified_at', 'created_at']


class ContactVerificationSerializer(serializers.ModelSerializer):
    verified_by_name = serializers.CharField(source='verified_by.username', read_only=True)
    officer_name = serializers.CharField(source='officer.name', read_only=True)
    
    class Meta:
        model = ContactVerification
        fields = ['id', 'officer', 'officer_name', 'verified_by_name', 
                  'is_correct', 'notes', 'verified_at']
        read_only_fields = ['verified_at']


class EscalationLadderSerializer(serializers.Serializer):
    """
    Custom serializer for the escalation ladder view
    """
    level = serializers.IntegerField()
    designation = DesignationSerializer()
    officer = OfficerSerializer(allow_null=True)
