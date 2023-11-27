from rest_framework import serializers
from .models import Center, Department, ProblemType, Staff, Expert, Problem, FileAttachment, Notification, Comment

# Center Serializer
class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'

# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

# ProblemType Serializer
class ProblemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = '__all__'

# Problem History Serializer
class ProblemHistorySerializer(serializers.ModelSerializer):
    expert_name = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ['title', 'submission_date', 'expert_name']

    def get_expert_name(self, obj):
        return f"{obj.expert.name} {obj.expert.surname}" if obj.expert else None
        
# Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

# Expert Serializer
class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'

# Problem Serializer
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

# FileAttachment Serializer
class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = ['problem', 'staff', 'file_path', 'file_type', 'file_size']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
