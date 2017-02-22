"""
Definition of views.
"""

from app import forms
from app import models
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from urllib.parse import urlparse
import requests
import xml.etree.ElementTree as ET


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
#Рендер страницы с командами TODO:Полнотекстовый поиск
def teams(request):
    #assert  isinstance(request, HttpRequest)
    try:
        n = int(request.GET['n'])
        e = int(request.GET['e'])
    except Exception:
        n = 0
        e = 20
    mod = models.Team.objects.filter(enabled=True)
    co = mod.count()
    mod = mod.order_by('registered')[n:e]
    return render(
        request,
        'app/teams.html',
        {
            'title':'Teams',
            'teams':mod,
            'count':co,
            'n':n,
            'e':e,
            'nb':n-20,
            'eb':e-20,
            'ne':co-20,
            'nn':n+20,
            'en':e+20,
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
            url = urlparse(form.cleaned_data['team_url'])
            bad = True
            steamid = 0
            if url.netloc == 'steamcommunity.com' and url.path[:8] == '/groups/' and url.path.rfind('/') == 7:
                try:
                    che = url.geturl() + '/memberslistxml/?xml=1'
                    ans = requests.get(che)
                    ans = ET.fromstring(ans.content)
                    steamid = int(ans.find('groupID64').text)
                    ans = ans.find('groupDetails')
                    imgurl = ans.find('avatarMedium').text
                    bad = False
                except Exception:
                    bad = True


            if text[0] > 30:
                return render(request, 'app/text.html', { 'title':'Ошибка', 'text':'Какое-то слово(а) в вашем описании'
                                                                         ' больше 30 символов.' })
            elif bad:
                return  render(request, 'app/text.html', { 'title':'Ошибка', 'text':'Проверьте формат ссылки на группу в'
                                                                                    ' Steam. Например: http://steamcommunity.com/groups/potatogroup'})
            elif models.Team.objects.filter(owner=request.user).count() >= 2:
                return  render(request, 'app/text.html', { 'title':'Ошибка', 'text':'Не более 2-х команд на аккаунт'})
            else:
            # process the data in form.cleaned_data as required
                tm = models.Team(
                    name=form.cleaned_data['team_name'],
                    owner=request.user,
                    founded=form.cleaned_data['founded'],
                    description=form.cleaned_data['description'],
                    team_url=steamid,
                    image = imgurl,
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
#ЛК
def myposts(request):
    try:
        mod = models.Team.objects.filter(enabled=True, owner=request.user)
        return render(request, 'app/posts.html', {'title':'Мои объявления', 'teams':mod})
    except Exception:
        return render(request, 'app/text.html', {'title':'Ошибка', 'text':'Не найденно команд или не выполнен вход'})
def delete(request):
    try:
        id = int(request.GET['id'])
        mod = models.Team.objects.filter(id=id, owner=request.user)
        for i in mod:
            i.delete()
        return redirect('/myposts')
    except Exception:
        return render(request, 'app/text.html', {'title':'Ошибка', 'text':'Такой команды не существует либо она не принадлежит пользователю.'})