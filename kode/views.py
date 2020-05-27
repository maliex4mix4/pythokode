from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import sys
from . import forms
from django.contrib.messages import success
from django.contrib.messages import error
from .models import CodeProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, Count

@login_required(login_url='users:login')
def home_default(request):

	return render(request, 'kode/home.html', {'output': 'None', 'input': 'None'})

@login_required(login_url='users:login')
def run_code(request):


	if request.method == 'POST':

		filedir = 'static/output-files/file-'+request.user.username+'.txt'
		_code = request.POST['code_body']
		input_part = request.POST['code_inpt']
		default_code_point = 10

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
			exitx = CodeProfile.objects.filter(user=request.user, code_body=_code)
			if len(exitx) > 1:
				default_code_point = 0
			CodeProfile.objects.create(user=request.user, code_body=_code, code_inputs=y, code_outputs=output, code_points=default_code_point)

		except Exception as e:

			sys.stdout.close()
			sys.stdout = orig_std
			output = e

		msg = 'Code run successfully! you were awarded '+str(default_code_point)+' points :)'
		success(request, msg, fail_silently=False)


	context = {
		'output': output,
		'input': y,
		'body': _code
	}

	return render(request, 'kode/home.html', context)

@login_required(login_url='users:login')
def history(request, user):

	page = request.GET.get('page', 1)
	user = User.objects.get(username=user)
	hist = CodeProfile.objects.filter(user=user.id).order_by('-date_posted')
	paginator = Paginator(hist, 5)
	try:
		hist = paginator.page(page)
	except PageNotAnInteger:
		hist = paginator.page(1)
	except EmptyPage:
		hist = paginator.page(paginator.num_pages)

	return render(request, 'kode/code-history.html', {'histories': hist,})

@login_required(login_url='users:login')
def leaderboard(request):

	page = request.GET.get('page', 1)
	users = CodeProfile.objects.values('user__username').annotate(sum=Sum('code_points'), count=Count('code_body')).order_by('-sum')
	paginator = Paginator(users, 10)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	return render(request, 'kode/leaderboard.html', {'users':users,})
