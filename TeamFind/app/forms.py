# coding=utf-8
"""
Definition of forms.
"""
from datetime import datetime

from django import forms
from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from captcha.fields import ReCaptchaField

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

#Описание формы команд
class AddTeamForm(forms.Form):
    team_name = forms.CharField(label='Название команды', max_length=19, required=True)
    description = forms.CharField(widget=forms.Textarea, label='Описание команды', max_length=500, required=True)
    team_url = forms.URLField(label='Ссылка на группу в Steam', required=True)
    founded = forms.DateField(label='Основана', required=True, initial=datetime.now())
    min_rank = forms.ChoiceField(choices=settings.RANKS, label='Минимальный ранг', initial='UN')
    max_rank = forms.ChoiceField(choices=settings.RANKS, label='Максимальный ранг', initial='GE')
    is_mm = forms.BooleanField(label=settings.TYPES[settings.TYPES_SETTINGS['MM']][1], initial=True, required=False)
    is_pu = forms.BooleanField(label=settings.TYPES[settings.TYPES_SETTINGS['PU']][1], initial=False, required=False)
    is_le = forms.BooleanField(label=settings.TYPES[settings.TYPES_SETTINGS['LE']][1], initial=False, required=False)
    is_ca = forms.BooleanField(label=settings.TYPES[settings.TYPES_SETTINGS['CA']][1], initial=True, required=False)
    need_awp = forms.BooleanField(label='Требуется ' + settings.GAMERS['AWP'], initial=True, required=False)
    need_luk = forms.BooleanField(label='Требуется ' + settings.GAMERS['LUK'], initial=True, required=False)
    need_rif = forms.BooleanField(label='Требуется ' + settings.GAMERS['RIF'], initial=True, required=False)
    need_igl = forms.BooleanField(label='Требуется ' + settings.GAMERS['IGL'], initial=True, required=False)
    need_sup = forms.BooleanField(label='Требуется ' + settings.GAMERS['SUP'], initial=True, required=False)
    need_frg = forms.BooleanField(label='Требуется ' + settings.GAMERS['FRG'], initial=True, required=False)
    captcha = ReCaptchaField()