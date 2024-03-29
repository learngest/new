# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm
from django.conf import settings

from coaching.models import Client, Groupe, Utilisateur, Administrateurs, Assistants, Groupes

from listes import *

admin.site.unregister(User)
admin.site.unregister(Group)

class ClientAdmin(admin.ModelAdmin):
    search_fields = ('nom',)
admin.site.register(Client, ClientAdmin)

class AssistantFormset(ModelForm):
    utilisateur = forms.ModelChoiceField(label='Assistant',
            queryset=Utilisateur.objects.filter(statut__gte=ASSISTANT))

    class Meta:
        model = Assistants

class AssistantsDuGroupeInline(admin.TabularInline):
    model = Assistants
    verbose_name = 'Assistant'
    verbose_name_plural = _('Group assistants')

    def get_formset(self, request, obj=None, **kwargs):
        if obj is not None:
            self.form = AssistantFormset
        return super(AssistantsDuGroupeInline,
                    self).get_formset(request, obj, **kwargs)

class AdministrateursFormset(ModelForm):
    utilisateur = forms.ModelChoiceField(label='Administrateur',
            queryset=Utilisateur.objects.filter(statut__gte=ADMIN))

    class Meta:
        model = Assistants

class AdministrateursDuGroupeInline(admin.TabularInline):
    model = Administrateurs
    verbose_name = _('Manager')
    verbose_name_plural = _('Group managers')

    def get_formset(self, request, obj=None, **kwargs):
        if obj is not None:
            self.form = AdministrateursFormset
        return super(AdministrateursDuGroupeInline,
                self).get_formset(request, obj, **kwargs)

class GroupeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('nom',)}),
        (None, {'fields': ('client',)}),
    )
    list_display = ('id','client','nom',)
    list_filter = ('client',)
    search_fields = ('nom',)
    inlines = (AdministrateursDuGroupeInline, AssistantsDuGroupeInline,)

#    def nom_url(self, obj):
#        return "<a href=\"%s\">%s</a>" % (
#                obj.get_absolute_url(), obj.nom)
#    nom_url.short_description = _('Name')
#    nom_url.admin_order_field = 'nom'
#    nom_url.allow_tags = True

admin.site.register(Groupe, GroupeAdmin)

class GroupesInline(admin.TabularInline):
    model = Groupes
    verbose_name = _('Group')

class UtilisateurAdminForm(ModelForm):
    email = forms.EmailField(label=_("Email"), max_length=75)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput,
            required=False)
    password2 = forms.CharField(label=_("Password confirmation"), 
            widget=forms.PasswordInput, required=False)

    class Meta:
        model = Utilisateur
        exclude = ('password', 'username')

    def clean_email(self):
        self.email = self.cleaned_data["email"]
        user = super(UtilisateurAdminForm, self).save(commit=False)
        if Utilisateur.objects.filter( email=self.email).exclude(username=user.username).count():
            raise forms.ValidationError(_("A user with that email already exists."))
        return self.email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UtilisateurAdminForm, self).save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UtilisateurCreationForm(ModelForm):
    username = forms.EmailField(label=_("Email"), max_length=75)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ("username",)

    def clean_username(self):
        self.email = self.cleaned_data["username"].lower()
        try:
            Utilisateur.objects.get(email=self.email)
        except Utilisateur.DoesNotExist:
            username = self.email.split('@')[0][:30]
            try:
                Utilisateur.objects.get(username=username)
            except Utilisateur.DoesNotExist:
                return username
        raise forms.ValidationError(_("A user with that email already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UtilisateurCreationForm, self).save(commit=False)
        user.email = self.email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UtilisateurAdmin(UserAdmin):
    form = UtilisateurAdminForm
    add_form = UtilisateurCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        (_("Identity"), 
                {'fields': ('last_name', 'first_name')}),
        (_("Parameters"), {'fields': ('statut', 'langue', 'fermeture')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#        (_('Groups'), {'fields': ('groups',)}),
    )
    list_display = ('id','full_name','statut','derniere_cnx')
    list_filter = ('statut',)
    list_display_links = ('id',)
    search_fields = ('email', 'last_name','first_name')
#    actions = ['send_an_email']
    inlines = (GroupesInline,)

#    def lookup_allowed(self, lookup, *args, **kwargs):
#        """
#        see http://www.hoboes.com/Mimsy/hacks/fixing-django-124s-suspiciousoperation-filtering/
#        """
#        if lookup.startswith(('groupe',)):
#            return True
#        return super(UtilisateurAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def derniere_cnx(self, obj):
        return obj.last_login.strftime('%Y-%m-%d')
    derniere_cnx.short_description = _('Last login')
    derniere_cnx.admin_order_field = 'last_login'

#    def groupe_short_name(self, obj):
#        return "<a href=\"%s\">%s</a>" % (
#                obj.groupe.get_absolute_url(), obj.groupe.nom[:19])
#    groupe_short_name.short_description = _('Group')
#    groupe_short_name.allow_tags = True
#    groupe_short_name.admin_order_field = 'groupe'
#
    def full_name(self, obj):
#        return "<a href=\"%s\">%s %s</a>" % (
#                obj.get_absolute_url(), obj.last_name, obj.first_name)
        return "%s %s" % (obj.last_name, obj.first_name)
    full_name.short_description = _('Name')
    full_name.admin_order_field = 'last_name'
    full_name.allow_tags = True
#
#    def cours_valides(self, obj):
#        return "%s / %s" % (obj.nb_cours_valides, obj.groupe.cours.count())
#    cours_valides.short_description = _('Completed courses')
#    cours_valides.admin_order_field = 'nb_cours_valides'
#
#    def modules_valides(self, obj):
#        return "%s / %s" % (obj.nb_valides, obj.nb_modules)
#    modules_valides.short_description = _('Validated modules')
#    modules_valides.admin_order_field = 'nb_valides'
#
#    def travaux_rendus(self, obj):
#        return "%s / %s" % (obj.nb_travaux_rendus,
#                Work.objects.filter(groupe=obj.groupe).count()) 
#    travaux_rendus.short_description = _('Uploaded assignments')
#    travaux_rendus.admin_order_field = 'nb_travaux_rendus'
#
#    send_an_email = send_email

admin.site.register(Utilisateur, UtilisateurAdmin)

