from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

	user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
	email = models.EmailField(unique=True)
	bio = models.TextField()

	def __str__(self):
		return self.email