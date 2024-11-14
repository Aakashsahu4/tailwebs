"""External Imports"""
from django.db import models

"""Internal Imports"""
from . import utils

class Subject(models.Model):
	"""Model to Store subjects Data"""

	name = models.CharField(max_length=30)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True,auto_now_add=False)
	modified = models.DateTimeField(auto_now=False,auto_now_add=True)

	def __str__(self):
		return self.name