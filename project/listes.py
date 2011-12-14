# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
        ('fr', _('French')),
        ('en', _('English')),
#        ('zh-cn', _('Simplified Chinese')),
)

LISTE_TYPES = (
        ('htm', 'HTML'),
        ('swf', 'Flash movie'),
        ('pdf', 'Portable Document Format'),
        ('doc', 'MS Word document'),
        ('xls', 'MS Excel document'),
)

(STUDENT, ASSISTANT, ADMIN, STAFF) = (0,10,30,40)

LISTE_STATUTS = (
        (STUDENT,'student'),
        (ASSISTANT,'assistant'),
        (ADMIN,'admin'),
        (STAFF,'staff'),
)

LISTE_TYPQ = (
        ('qcm', 'QCM'),
        ('qrm', 'QRM'),
        ('rnd', 'Question à valeurs aléatoires'),
        ('exa', 'Réponse exacte'),
        ('num', 'Réponse numérique, 5 chiffres significatifs'),
)
