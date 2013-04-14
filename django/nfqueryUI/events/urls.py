from django.conf.urls.defaults import *
from events import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
