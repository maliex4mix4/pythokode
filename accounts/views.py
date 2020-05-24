from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views import generic
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.contrib.messages import error
from . import forms
from django.contrib.auth.decorators import login_required


class Register(generic.CreateView):
    model = User
    template_name = 'accounts/register.html'
    success_url = 'login'
    form_class = UserCreationForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True



class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change-password.html'

@login_required(login_url='users:login')
def edit_profile(request):

	form = forms.ProfileCreate(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user

		instance.save()
		msg = 'Profile updated successfully!'
		success(request, msg, fail_silently=False)
		return redirect(request.path)

	context = {
		'username': 'malik',
		'form': form,
	}
	return render(request, 'accounts/edit_profile.html', context)
