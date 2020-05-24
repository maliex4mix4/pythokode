from django.forms import ModelForm
from .models import CodeProfile

class CodeProfileCreate(ModelForm):

	class Meta:

		model = CodeProfile
		fields = ['code_body', 'code_inputs', 'code_outputs']