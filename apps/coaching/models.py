# -*- encoding: utf-8 -*-
"""
Coaching app models

Copyright © 2011 Jean-Charles Bagneris. All Rights Reserved.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager

from email_auth.views import user_logged_in

from listes import *

def set_language(sender, **kwargs):
    """
    Récup le signal user_logged_in envoyé par email_auth
    Place la langue favorite du user dans la session
    """
    if hasattr(sender,'langue') and sender.langue:
        kwargs['request'].session['django_language'] = sender.langue

user_logged_in.connect(set_language)

class Client(models.Model):
    """
    Client model

    Defines CSS to use + free field for contacts etc.
    """

    nom = models.CharField(max_length=60, unique=True,
        help_text=_("Customer name, required."))
    style = models.CharField(_(u"Custom CSS"),
        max_length=20, null=True, blank=True,
        help_text=_("CSS to use with this customer."))
    contacts = models.TextField(null=True, blank=True,
        help_text=_("Free field (contacts, tel. numbers, ...)."))

    class Meta:
        ordering = ['nom']

    def __unicode__(self):
        return self.nom

class Groupe(models.Model):
    """
    Groupe model

    A Groupe belongs to one Client
    A Groupe has one or more Administrateur
    The Administrateur may change some properties of the Groupe itself,
    or the Utilisateur in this Groupe
    A Groupe has one or more Assistant
    The Assistant cannot change anything but can consult and download
    the marks and results of the Groupe's Utilisateur

    Note: the is_open flag does not exist anymore, as this will be
    specified for each activity
    """

    nom = models.CharField(max_length=60, unique=True,
        help_text=_("Group name, required."))
    client = models.ForeignKey(Client,
        help_text=_("Group customer, required."))

#    activite = models.ManyToManyField('Activites', blank=True, null=True,
#        through='ActivitesDuGroupe',
#        help_text=_("Courses or exams to which group members are subscribed."))

    administrateur = models.ManyToManyField('Utilisateur', blank=True, null=True,
        through='Administrateurs', related_name='administrateurs',
        help_text=_("Group admins"))

    assistant = models.ManyToManyField('Utilisateur', blank=True, null=True,
        through='Assistants', related_name='assistants',
        help_text=_("Group assistants"))

    class Meta:
        ordering = ['client', 'nom']

    def __unicode__(self):
        return "%s - %s" % (self.client.nom, self.nom)

    def get_admin_url(self):
        from django.core import urlresolvers
        return urlresolvers.reverse('admin:coaching_groupe_change',
                args=(str(self.id),))

    @models.permalink
    def get_absolute_url(self):
        return('coaching.views.groupe', [str(self.id)])

class Administrateurs(models.Model):
    """
    Administrateurs model

    An Administrateur is an Utilisateur
    The Administrateur may change some properties of a Groupe,
    or the Utilisateur in this Groupe
    """

    utilisateur = models.ForeignKey('Utilisateur', related_name='administrateur')
    groupe = models.ForeignKey(Groupe)

    class Meta:
        ordering = ('groupe',)
        verbose_name = 'Administrateur'
        verbose_name_plural = 'Administrateurs'

    def __unicode__(self):
        return "%s - %s" % (self.groupe, self.utilisateur)

class Assistants(models.Model):
    """
    Assistants model

    An Assistant is an Utilisateur
    The Assistant cannot change anything but can consult and download
    the marks and results of its Groupe's Utilisateur
    """

    utilisateur = models.ForeignKey('Utilisateur', related_name='assistant')
    groupe = models.ForeignKey(Groupe)

    class Meta:
        ordering = ('groupe',)
        verbose_name = 'Assistant'
        verbose_name_plural = 'Assistants'

    def __unicode__(self):
        return "%s - %s" % (self.groupe, self.utilisateur)

class Groupes(models.Model):
    """
    Groupes model

    M2M through field to associate an Utilisateur to the Groupes
    it belons to

    Deserialize here!
    """

    utilisateur = models.ForeignKey('Utilisateur',)
    groupe = models.ForeignKey(Groupe,related_name='u_groupes')

    class Meta:
        ordering = ('groupe',)
        verbose_name = 'Groupe'
        verbose_name_plural = 'Groupes'

    def __unicode__(self):
        return "%s - %s" % (self.groupe, self.utilisateur)

class Utilisateur(User):
    """
    Utilisateur model

    Based on the user model in contrib.auth
    """
    fermeture = models.DateTimeField(_("Expiration date"),
        blank=True, null=True,
        help_text=_("Account is valid till this date. Account is valid forever if empty."))
    langue = models.CharField(max_length=5, choices=LANGUAGES,
        default='fr',
        help_text=_(
        "User's prefered language for interface, messages and contents, required."))

    statut = models.IntegerField(choices=LISTE_STATUTS, default=0,
        help_text=_("User's status, required."))

    groupe = models.ManyToManyField(Groupe, blank=True, null=True,
        through='Groupes', related_name='groupes',
        help_text=_("User groups"))

    # on conserve le manager de l'objet User
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        ordering = ('statut',)

    def __unicode__(self):
        return self.email

    def get_admin_url(self):
        from django.core import urlresolvers
        return urlresolvers.reverse('admin:coaching_utilisateur_change',
                args=(str(self.id),))

    def may_see_groupe(self, grpe):
        """
        True if user may see group results
        """
        if self.is_staff:
            return True
        if self in grpe.administrateur.all():
            return True
        if self in grpe.assistant.all():
            return True
        return False

    def may_admin_groupe(self, grpe):
        """
        True if user may admin this group
        """
        if self.is_staff:
            return True
        if self in grpe.administrateur.all():
            return True
        return False

#    @models.permalink
#    def get_absolute_url(self):
#        return('coaching.views.user', [str(self.id)])

