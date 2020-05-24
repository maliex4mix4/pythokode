from django.db import models
from django.contrib.auth.models import User


class CodeProfile(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	code_body = models.TextField()
	code_inputs = models.TextField(default='None')
	code_outputs = models.TextField(default='None')
	date_posted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.code_body