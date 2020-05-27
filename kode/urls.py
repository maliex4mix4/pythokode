from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
	path('', views.home_default, name='home_default'),
	url(r'^run$', views.run_code, name='run_code'),
	url(r'^hist/(?P<user>[\w-]+)/$', views.history, name='code_history'),
	url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
]

app_name = 'kode'
