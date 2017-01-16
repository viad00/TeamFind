"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О сайте',
            'message':'Здесь размещена некоторая история о данном сервисе.',
            'year':datetime.now().year,
        }
    )

def players(request):
    assert  isinstance(request, HttpRequest)
    return render(
        request,
        'app/players.html',
        {
            'title':'Players',
            'year': datetime.now().year,
        }
    )

def teams(request):
    assert  isinstance(request, HttpRequest)
    return render(
        request,
        'app/teams.html',
        {
            'title':'Teams',
            'year': datetime.now().year,
        }
    )

def updateinfo(request):
    assert isinstance(request, HttpRequest)
    if (request.user.username != request.user.social_auth.get(provider='steam').extra_data['player']['steamid']):
        request.user.username = request.user.social_auth.get(provider='steam').extra_data['player']['steamid']
        request.user.save()
    return redirect('/')