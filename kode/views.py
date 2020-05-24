from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import sys
from . import forms
from django.contrib.messages import success
from django.contrib.messages import error
from .models import CodeProfile
from django.contrib.auth.models import User

@login_required(login_url='users:login')
def home_default(request):

	return render(request, 'kode/home.html', {'output': 'None', 'input': 'None'})

@login_required(login_url='users:login')
def run_code(request):


	if request.method == 'POST':
		
		filedir = 'static/output-files/file-'+request.user.username+'.txt'
		_code = request.POST['code_body']
		input_part = request.POST['code_inpt']

		y = input_part

		if input_part[:3] == 'None':
			input_part = input_part[3:]

		input_p = input_part.replace("\n"," ").split(" ")

		def input():
			a = input_p[0]
			del input_p[0]
			return a
		try:

			orig_std = sys.stdout
			sys.stdout = open(filedir, 'w')
			exec(_code)
			sys.stdout.close()
			sys.stdout = orig_std
			output = open(filedir, 'r').read()


		except Exception as e:

			sys.stdout.close()
			sys.stdout = orig_std
			output = e
		
		CodeProfile.objects.create(user=request.user, code_body=_code, code_inputs=y, code_outputs=output)

	context = {
		'output': output,
		'input': y,
		'body': _code
	}

	return render(request, 'kode/home.html', context)

def history(request, user):
	
	user = User.objects.get(username=user)
	hist = CodeProfile.objects.filter(user=user.id).order_by('-date_posted')
	return render(request, 'kode/code-history.html', {'histories': hist,})