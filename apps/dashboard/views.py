# -*- encoding: utf-8 -*-

import sys

#from django.template import RequestContext
#from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
#from django.core import urlresolvers

#from dashboard.planning import Calendrier, Planning
#from coaching.controllers import AdminGroupe, UserState
#from coaching.models import Groupe, Prof, AutresDocs

@login_required
def dashboard(request):
    """
    Wrapper pour les tableaux de bords des différents types
    d'utilisateurs :
    - staff
    - admin
    - prof
    - assistant
    - etudiant
    """
    return HttpResponseRedirect("/staff/")

