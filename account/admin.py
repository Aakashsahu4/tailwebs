"""External Imports"""
from django.contrib import admin

"""Internal Imports"""
from . import models


@admin.register(models.TeacherData)
class TeacherDataAdmin(admin.ModelAdmin):
	list_display = ['username']

@admin.register(models.StudentData)
class StudentDataAdmin(admin.ModelAdmin):
	list_display = ['name','subjects','mark']