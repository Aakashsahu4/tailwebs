"""External Imports"""
from django.db import models
from django.contrib.auth.models import AbstractUser

"""Internal Imports"""
from master import utils as master_utils
from master import models as master_models

class TeacherData(AbstractUser):
	"""Model to Store Teachers Data"""

	password = models.CharField(max_length=10)

	def __str__(self):
		return self.username



class StudentData(models.Model):
	"""Model to store all Students Data"""

	name = models.CharField(max_length=30)
	subjects = models.ForeignKey(master_models.Subject,on_delete=models.CASCADE,related_name='master_subject')
	mark = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.name