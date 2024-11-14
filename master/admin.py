"""External Imports"""
from django.contrib import admin

"""Internal Imports"""
from . import models


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ['name','created','modified']