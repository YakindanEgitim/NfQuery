from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nfqueryUI.lib.rpc.rpcutils import get_total_severity_from_queryserver, get_hosts_from_queryserver
from django.utils import simplejson
from django.utils.decorators import method_decorator


@login_required
def get_severity(request):
    host = request.GET.get("host")
    latest_timestamp = request.GET.get("latest_timestamp")
    log = get_total_severity_from_queryserver(latest_timestamp, host)

    return HttpResponse(simplejson.dumps(log), mimetype='application/json')

@login_required
def index(request):
    data = {'tabName': "events", 'pageTitle': "Events"}
    data['hosts'] = get_hosts_from_queryserver()
    return render_to_response('events/events.html', data, context_instance=RequestContext(request))
