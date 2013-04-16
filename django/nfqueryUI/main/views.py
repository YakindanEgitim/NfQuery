from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

def login_user(request):
    data = {'pageTitle': _('Login')}
    return render_to_response('main/login.html', data, context_instance=RequestContext(request))
