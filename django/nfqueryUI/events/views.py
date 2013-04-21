from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    data = {'tabName': "events", 'pageTitle': "Events"}
    return render_to_response('base/layout.html', data, context_instance=RequestContext(request))
