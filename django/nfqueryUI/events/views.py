from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nfqueryUI.lib.rpc.rpcutils import get_log
import sys

@login_required
def index(request):
    data = {'tabName': "events", 'pageTitle': "Events"}
    #log = get_log()
    #data['log'] = log
    return render_to_response('events/events.html', data, context_instance=RequestContext(request))
