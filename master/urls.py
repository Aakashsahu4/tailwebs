"""External Imports"""
from django.urls import path

"""Internal Imports"""
from . import views



urlpatterns = [
	path('api/subjects-list/',views.SubjectListAPI.as_view()),
]