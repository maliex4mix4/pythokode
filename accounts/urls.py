from django.urls import path

from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('change-password', views.ChangePasswordView.as_view(), name='change_password'),
]
app_name = 'users'
