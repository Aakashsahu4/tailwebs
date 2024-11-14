"""External Imports"""
from rest_framework import serializers

"""Internal Imports"""
from . import models


class SubjectSerializer(serializers.ModelSerializer):
	"""Serializer for Subject Table"""

	class Meta:
		model = models.Subject
		fields = ['id','name']