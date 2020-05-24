from django.forms import ModelForm
from accounts.models import UserProfile

class ProfileCreate(ModelForm):

	class Meta:

		model = UserProfile
		fields = ['email', 'bio',]