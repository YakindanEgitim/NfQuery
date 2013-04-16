from django.conf.urls.defaults import *
from main import views

urlpatterns = patterns('',
    url(r'^$', views.login_user, name='login'),
)
