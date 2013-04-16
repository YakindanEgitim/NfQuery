from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login
from django.utils.translation import ugettext as _
from main.forms import LoginForm

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('events:index'))
    data = {'pageTitle': _('Login')}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('events:index'))
                else:
                    print "a"
                    data['form'] = form
                    return render_to_response('main/login.html', data, context_instance=RequestContext(request))
            else:
                print "aa"
                data['form'] = form
                return render_to_response('main/login.html', data, context_instance=RequestContext(request))
        else:
            print "aaa"
            data['form'] = form
            return render_to_response('main/login.html', data, context_instance=RequestContext(request))
    else:
        data['form'] = LoginForm()
        return render_to_response('main/login.html', data, context_instance=RequestContext(request))
