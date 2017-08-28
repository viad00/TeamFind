"""
Definition of urls for TeamFind.
"""

from datetime import datetime

from django.conf import settings
from django.conf.urls import url, include
import django.contrib.auth.views
from django.shortcuts import redirect

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^players', app.views.players, name='players'),
    url(r'^teams', app.views.teams, name='teams'),
    url(r'^teamd', app.views.teamd, name='teamd'),
    url(r'^updateinfo', app.views.updateinfo, name='updateinfo'),
    url(r'^myposts', app.views.myposts, name='myposts'),
    url(r'^delete', app.views.delete, name='delete'),
    url(r'^update', app.views.update, name='update'),
    url(r'^crondis', app.views.crondis, name='crondis'),
    url(r'^help', app.views.help, name='help'),
    url(r'^sitemap.xml', app.views.sitemap, name='sitemap'),
    url(r'^viewteam', app.views.viewteam, name='viewteam'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^addteam', app.views.addteam),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url('', include('social_django.urls', namespace='social')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns