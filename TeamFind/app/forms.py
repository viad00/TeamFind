# coding=utf-8
"""
Definition of forms.
"""
from datetime import datetime
from app import strings
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
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
    team_name = forms.CharField(label=_('Название команды'), max_length=18, required=True)
    description = forms.CharField(widget=forms.Textarea, label=_('Описание команды'), max_length=500, required=True)
    team_url = forms.URLField(label=_('Ссылка на группу в Steam'), required=True)
    founded = forms.DateField(label=_('Основана'), required=True, initial=datetime.now())
    min_rank = forms.ChoiceField(choices=strings.RANKS, label=_('Минимальный ранг'), initial='UN')
    max_rank = forms.ChoiceField(choices=strings.RANKS, label=_('Максимальный ранг'), initial='GE')
    is_mm = forms.BooleanField(label=strings.TYPES['MM'], initial=True, required=False)
    is_pu = forms.BooleanField(label=strings.TYPES['PU'], initial=False, required=False)
    is_le = forms.BooleanField(label=strings.TYPES['LE'], initial=False, required=False)
    is_ca = forms.BooleanField(label=strings.TYPES['CA'], initial=True, required=False)
    need_awp = forms.BooleanField(label=_('Требуется ') + strings.GAMERS['AWP'], initial=True, required=False)
    need_luk = forms.BooleanField(label=_('Требуется ') + strings.GAMERS['LUK'], initial=True, required=False)
    need_rif = forms.BooleanField(label=_('Требуется ') + strings.GAMERS['RIF'], initial=True, required=False)
    need_igl = forms.BooleanField(label=_('Требуется ') + strings.GAMERS['IGL'], initial=True, required=False)
    need_sup = forms.BooleanField(label=_('Требуется ') + strings.GAMERS['SUP'], initial=True, required=False)
    need_frg = forms.BooleanField(label=_('Требуется ') + strings.GAMERS['FRG'], initial=True, required=False)
    captcha = ReCaptchaField()
