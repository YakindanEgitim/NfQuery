from django.conf.urls.defaults import *
from main import views

urlpatterns = patterns('',
    url(r'^$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
)
