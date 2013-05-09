from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nfqueryUI.lib.rpc.rpcutils import get_severtiy_from_query_server
from django.utils import simplejson
from django.utils.decorators import method_decorator


@login_required
def get_severity(request):
    log = get_severtiy_from_query_server()
    return HttpResponse(simplejson.dumps(log), mimetype='application/json')

@login_required
def index(request):
    data = {'tabName': "events", 'pageTitle': "Events"}
    return render_to_response('events/events.html', data, context_instance=RequestContext(request))
