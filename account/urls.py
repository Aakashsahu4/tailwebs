"""External Imports"""
from django.urls import path

"""Internal Imports"""
from . import views



urlpatterns = [
	path('api/create-teacher/',views.CreateTeacherAPI.as_view(),name='create-teacher'),
	path('api/login/',views.TeacherLoginAPI.as_view(),name='login'),
	path('api/forgot-password/',views.ForgotPasswordAPI.as_view(), name='forgot-password'),
	path('api/create-student/',views.CreateStudentDataAPI.as_view(), name='create-student'),
	path('api/students-list/',views.StudentsListAPI.as_view(), name='students-list'),
	path('api/edit-student/<int:id>/',views.EditStudentData.as_view(), name='edit-student'),
	path('api/delete-student/<int:id>/',views.DeleteStudentData.as_view(), name='delete-student'),
]

