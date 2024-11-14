"""External Imports"""
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q

"""Internal Imports"""
from . import models, serializers
from master.utils import CustomResponses, PasswordRecover
from master import messages, keys
from master import models as master_models



class CreateTeacherAPI(APIView):
	"""API to create a new teacher Data"""

	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')

		if username and password:
			teacher_instance = models.TeacherData.objects.filter(username=username)
			if teacher_instance:
				return Response(CustomResponses.failure_reponse(messages.TEACHER_EXISTS,[]),status=status.HTTP_400_BAD_REQUEST)
			serializer = serializers.TeacherSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(CustomResponses.success_reponse(messages.TEACHER_CREATED,serializer.data),status=status.HTTP_200_OK)
			return Response(CustomResponses.serializer_error_message_function(serializer.errors),status=status.HTTP_400_BAD_REQUEST)
		return Response(CustomResponses.failure_reponse(messages.DATA_REQUIRED,[]),status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginAPI(APIView):
	"""API for teacher Login"""

	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')

		if request.data:
			teacher_instance = models.TeacherData.objects.filter(username=username,password=password)
			if teacher_instance:
				refresh = RefreshToken.for_user(teacher_instance.last())
				access_token = refresh.access_token
				return Response({
					keys.ACCESS_TOKEN: str(access_token),
					keys.REFRESH_TOKEN: str(refresh),
				})
			return Response(CustomResponses.failure_reponse(messages.INVALID_CREDENTIALS,[]), status=status.HTTP_400_BAD_REQUEST)
		return Response(CustomResponses.failure_reponse(messages.DATA_REQUIRED,[]),status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPI(APIView):
	"""API for recovering teacher Login password"""

	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')

		if request.data:
			teacher_instance = models.TeacherData.objects.filter(username=username)
			if teacher_instance:
				password_hint = PasswordRecover.obscure_password(teacher_instance.last().password)
				return Response(CustomResponses.success_reponse(messages.PASSWORD_RECOVERY,password_hint))
			return Response(CustomResponses.failure_reponse(messages.USERNAME_NOT_EXIST,[]), status=status.HTTP_400_BAD_REQUEST)
		return Response(CustomResponses.failure_reponse(messages.DATA_REQUIRED,[]),status=status.HTTP_400_BAD_REQUEST)
	


class CreateStudentDataAPI(APIView):
    """API to create or update a new Student Data"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        subject_id = request.data.get('subject_id')
        mark = request.data.get('mark')

        if not name or not subject_id or not mark:
            return Response(CustomResponses.failure_reponse(messages.DATA_REQUIRED, []),status=status.HTTP_400_BAD_REQUEST)

        subject_ = master_models.Subject.objects.filter(id=subject_id).last()
        if not subject_:
            return Response(CustomResponses.failure_reponse(messages.SUBJECT_NOT_FOUND, []),status=status.HTTP_400_BAD_REQUEST)

        student_instance = models.StudentData.objects.filter(name=name, subjects=subject_).first()
        
        if student_instance:
            student_instance.mark = mark
            student_instance.save()
            return Response(CustomResponses.success_reponse(messages.STUDENT_UPDATED, []),status=status.HTTP_200_OK)
        
        serializer = serializers.StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponses.success_reponse(messages.STUDENT_CREATED, serializer.data),status=status.HTTP_200_OK)
        
        return Response(CustomResponses.serializer_error_message_function(serializer.errors),status=status.HTTP_400_BAD_REQUEST)


class StudentsListAPI(APIView):
	"""API to list down all the Students"""

	permission_classes = [IsAuthenticated]

	def get(self, request):
		search_query = request.GET.get('search',None)
		page = request.GET.get('page_number', 1)
		page_count = request.GET.get('page_count',5)

		if search_query:
			student_data = models.StudentData.objects.filter(Q(name__icontains=search_query)).order_by('-created')
			paginator = Paginator(student_data,page_count)
			result = paginator.page(page)

			if student_data is not None:
				serializer = serializers.StudentSerializer(result,many=True,context={"request":request})
				return Response(CustomResponses.pagination_response(paginator,page,page_count,serializer.data),status=status.HTTP_200_OK)

		students_query = models.StudentData.objects.all().order_by('-created')
		paginator = Paginator(students_query, page_count)
		result = paginator.page(page)
		serializer = serializers.StudentSerializer(result, many=True)
		return Response(CustomResponses.pagination_response(paginator,page,page_count,serializer.data),status=status.HTTP_200_OK)


class EditStudentData(APIView):
    """API to edit student details"""

    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return models.StudentData.objects.get(id=id)
        except models.StudentData.DoesNotExist:
            return None

    def patch(self, request, id):
        student_instance = self.get_object(id)
        if student_instance is None:
            return Response(CustomResponses.failure_reponse(messages.STUDENT_NOT_FOUND, []), status=status.HTTP_400_BAD_REQUEST)

        subject_id = request.data.get('subject_id')
        if subject_id:
            subject = master_models.Subject.objects.filter(id=subject_id).last()
            if not subject:
                return Response(CustomResponses.failure_reponse(messages.SUBJECT_NOT_FOUND, []), status=status.HTTP_400_BAD_REQUEST)
            student_instance.subjects = subject

        serializer = serializers.StudentSerializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponses.success_reponse(messages.STUDENT_UPDATED, serializer.data), status=status.HTTP_200_OK)

        return Response(CustomResponses.serializer_error_message_function(serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class DeleteStudentData(APIView):
	"""API to delete student Data"""

	permission_classes = [IsAuthenticated]

	def get_object(self, id):
		try:
			return models.StudentData.objects.get(id=id)
		except models.StudentData.DoesNotExist:
			return None

	def delete(self, request, id):
		student_data = self.get_object(id)
		if student_data is None:
			return Response(CustomResponses.failure_reponse(messages.STUDENT_NOT_FOUND,[]),status=status.HTTP_404_NOT_FOUND)

		student_data.delete()
		return Response(CustomResponses.success_reponse(messages.STUDENT_DATA_DELETED,[]),status=status.HTTP_200_OK)