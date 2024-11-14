"""Utils file for all reusable datas"""

"""External Imports"""
from django.db import models

"""Internal Imports"""
from . import keys


class CustomResponses():
	"""Custom responses"""

	@staticmethod
	def success_reponse(message,data):
		response_data={
			keys.SUCCESS:True,
			keys.MESSAGE : message,
			keys.DATA :data,
				}
		return response_data

	@staticmethod
	def failure_reponse(message,data):
		response_data={
			keys.SUCCESS:False,
			keys.MESSAGE : message,
			keys.DATA :data,
				}
		return response_data

	@staticmethod
	def serializer_error_message_function(errors):
		"""
		return error message when serializer is not valid
		:param errors: error object
		:returns: string
		"""
		for key, values in errors.items():
			error = [value[:] for value in values]
			err = ' '.join(map(str,error))
			return err
	
	@staticmethod
	def pagination_response(paginator,page,page_count,data):
		Response={
			keys.SUCCESS:True,
			keys.DATA: data,
			keys.PAGE_NUMBER: int(page),
			keys.TOTAL_PAGE: paginator.num_pages,
			keys.PAGE_COUNT: int(page_count),
			keys.TOTAL_COUNT: paginator.count,
		}
		return Response


class PasswordRecover():
	def obscure_password(password):
		if len(password) <= 4:
			return password[:1] + '*' * (len(password) - 2) + password[-1:]
		else:
			return password[:2] + '*' * (len(password) - 4) + password[-2:]