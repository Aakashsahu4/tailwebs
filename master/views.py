"""External Imports"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

"""Internal Imports"""
from . import models, serializers
from master.utils import CustomResponses
from master import messages, keys


class SubjectListAPI(APIView):
	"""API to list all the Subjects"""


	def get(self, request):
		subjects_query = models.Subject.objects.all()
		serializer = serializers.SubjectSerializer(subjects_query, many=True)
		return Response(CustomResponses.success_reponse(messages.SUBJECT_LIST,serializer.data),status=status.HTTP_200_OK)
