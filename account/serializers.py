"""External Imports"""
from rest_framework import serializers

"""Internal Imports"""
from . import models
from master import models as master_models


class TeacherSerializer(serializers.ModelSerializer):
	"""Serializer for Teacher Table"""

	class Meta:
		model = models.TeacherData
		fields = ['username','password']

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student Data Table"""

    subject_id = serializers.IntegerField(write_only=True)
    subjects = serializers.CharField(source='subjects.name', read_only=True)

    class Meta:
        model = models.StudentData
        fields = ['id', 'name', 'subject_id', 'subjects', 'mark']

    def create(self, validated_data):
        subject_id = validated_data.pop('subject_id')
        subject = master_models.Subject.objects.get(id=subject_id)
        student = models.StudentData.objects.create(subjects=subject, **validated_data)
        return student
    
    def update(self, instance, validated_data):
        subject_id = validated_data.get('subject_id', None)
        if subject_id:
            subject = master_models.Subject.objects.get(id=subject_id)
            instance.subjects = subject
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
