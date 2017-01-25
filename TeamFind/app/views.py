"""
Definition of views.
"""

from datetime import datetime

from app import forms
from app import models
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
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
            #'message': request.user.social_auth.get(provider='steam').extra_data['player']['personaname'],
        }
    )
#Рендер страницы с игроками TODO:Players
def players(request):
    assert  isinstance(request, HttpRequest)
    return render(
        request,
        'app/players.html',
        {
            'title':'Players',
        }
    )
#Рендер страницы с командами TODO:Полнотекстовый поиск, обработку кол-ва страниц
def teams(request):
    assert  isinstance(request, HttpRequest)
    ass = 20
    mod = models.Team.objects.filter(enabled=True).order_by('registered')[:ass]
    return render(
        request,
        'app/teams.html',
        {
            'title':'Teams',
            'teams':mod,
            'count':models.Team.objects.count(),
        }
    )
#Страница для обновления информации о клиенте
def updateinfo(request):
    assert isinstance(request, HttpRequest)
    if (request.user.get_username() != request.user.social_auth.get(provider='steam').extra_data['player']['steamid']):
        request.user.username = request.user.social_auth.get(provider='steam').extra_data['player']['steamid']
        request.user.save()
    return redirect('/')
#Форма для добавления игрока
def addteam(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.AddTeamForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            text = form.cleaned_data['description']
            text = list(map(len, text.split()))
            text.sort(reverse=True)
            if text[0] > 30:
                return render(request, 'app/text.html', { 'title':'Ошибка', 'text':'Какое-то слово(а) в вашем описании'
                                                                                   ' больше 30 символов.' })
            else:
            # process the data in form.cleaned_data as required
                tm = models.Team(
                    name=form.cleaned_data['team_name'],
                    owner=request.user,
                    founded=form.cleaned_data['founded'],
                    description=form.cleaned_data['description'],
                    team_url=form.cleaned_data['team_url'],
                    min_rank=form.cleaned_data['min_rank'],
                    max_rank=form.cleaned_data['max_rank'],
                    is_mm=form.cleaned_data['is_mm'],
                    is_pu=form.cleaned_data['is_pu'],
                    is_le=form.cleaned_data['is_le'],
                    is_ca=form.cleaned_data['is_ca'],
                )
                tm.save()
                #return render(request, 'app/text.html', {'text': })
                # redirect to a new URL:
                return HttpResponseRedirect('/teams')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.AddTeamForm

    return render(request, 'app/addteam.html', {'title':'Добавить команду', 'form': form})
