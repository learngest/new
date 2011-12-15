# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.translation import activate, ugettext as _
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings

from coaching.forms import UtilisateurChangeForm

from listes import *

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

@login_required
def profile(request):
    """
    Modifier le compte Utilisateur.
    Les champs que l'Utilisateur peut changer sont :
    - password
    - langue
    """
    if request.method == "POST":
        form = UtilisateurChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.session['django_language'] = request.user.langue
            activate(request.user.langue)
            request.user.message_set.create(
                    message=_("Changes saved successfully."))
            return HttpResponseRedirect(LOGIN_REDIRECT_URL)
        else:
            return render_to_response('coaching/change_profile.html', {
                'form': form,
                'here':'profile',
            }, context_instance=RequestContext(request))
    else:
        form = UtilisateurChangeForm(instance=request.user)
    return render_to_response('coaching/change_profile.html', {
        'title': _('Change account'),
        'form': form,
        'here':'profile',
    }, context_instance=RequestContext(request))
    

