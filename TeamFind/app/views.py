"""
Definition of views.
"""
import calendar

import django
from app import forms
from app import models
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from urllib.parse import urlparse
import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from django.utils.datetime_safe import datetime
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
@vary_on_cookie
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    cc = models.Team.objects.count()
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'count':cc,
        }
    )

@cache_page(CACHE_TTL)
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

@cache_page(CACHE_TTL)
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

@cache_page(CACHE_TTL)
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
@cache_page(CACHE_TTL)
def teams(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/teams.html',
        {
            'title': 'Teams',
            'is_mm': settings.TYPES[settings.TYPES_SETTINGS['MM']][1],
            'is_pu': settings.TYPES[settings.TYPES_SETTINGS['PU']][1],
            'is_le': settings.TYPES[settings.TYPES_SETTINGS['LE']][1],
            'is_ca': settings.TYPES[settings.TYPES_SETTINGS['CA']][1],
            'gamers':settings.GAMERS,
        }
    )

@cache_page(CACHE_TTL)
@vary_on_cookie
def teamd(request):
    assert isinstance(request, HttpRequest)
    try:
        n = int(request.GET['n'])
        e = int(request.GET['e'])
    except Exception:
        n = 0
        e = 20
    if e-n > 50 or e-n < 3:
        n=0
        e=20
    mod = models.Team.objects.filter(enabled=True)
    try:
        if request.COOKIES['show_mm'] == '0':
            mod = mod.filter(is_mm=False)
        elif request.COOKIES['show_mm'] == '1':
            mod = mod.filter(is_mm=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['show_pu'] == '0':
            mod = mod.filter(is_pu=False)
        elif request.COOKIES['show_pu'] == '1':
            mod = mod.filter(is_pu=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['show_le'] == '0':
            mod = mod.filter(is_le=False)
        elif request.COOKIES['show_le'] == '1':
            mod = mod.filter(is_le=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['show_ca'] == '0':
            mod = mod.filter(is_ca=False)
        elif request.COOKIES['show_ca'] == '1':
            mod = mod.filter(is_ca=True)
    except Exception:
        mm = True
    try:
        for rank in settings.RANKS:
            if request.COOKIES['ex_'+rank[0]] == '1':
                mod = mod.exclude(min_rank=rank[0])
                mod = mod.exclude(max_rank=rank[0])
    except Exception:
        mm = True
    try:
        if request.COOKIES['need_awp'] == 'true':
            mod = mod.filter(need_awp=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['need_luk'] == 'true':
            mod = mod.filter(need_luk=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['need_rif'] == 'true':
            mod = mod.filter(need_rif=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['need_igl'] == 'true':
            mod = mod.filter(need_igl=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['need_sup'] == 'true':
            mod = mod.filter(need_sup=True)
    except Exception:
        mm = True
    try:
        if request.COOKIES['need_frg'] == 'true':
            mod = mod.filter(need_frg=True)
    except Exception:
        mm = True
    mod = mod.order_by('-registered')[n:e]
    
    return render(
        request,
        'app/teamsnum.html',
        {
            'teams':mod,
            'is_mm':settings.TYPES[settings.TYPES_SETTINGS['MM']][1],
            'is_pu':settings.TYPES[settings.TYPES_SETTINGS['PU']][1],
            'is_le':settings.TYPES[settings.TYPES_SETTINGS['LE']][1],
            'is_ca':settings.TYPES[settings.TYPES_SETTINGS['CA']][1],
            'ranks':settings.RANKS,
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
            text = form.cleaned_data['description'].lower()
            name = form.cleaned_data['team_name'].lower()
            badword = False
            words = []
            for word in models.BadWords.objects.all():
                if word.word in text:
                    badword = True
                    words.append(word.word)
                elif word.word in name:
                    badword = True
                    words.append(word.word)
            text = list(map(len, text.split()))
            text.sort(reverse=True)
            url = urlparse(form.cleaned_data['team_url'])
            bad = True
            steamid = 0
            if url.netloc == 'steamcommunity.com' and url.path[:8] == '/groups/' and url.path.rfind('/') == 7:
                try:
                    che = 'https://steamcommunity.com' + url.path + '/memberslistxml/?xml=1'
                    ans = requests.get(che)
                    ans = ET.fromstring(ans.content)
                    steamid = int(ans.find('groupID64').text)
                    ans = ans.find('groupDetails')
                    imgurl = ans.find('avatarFull').text
                    bad = False
                except Exception:
                    bad = True

            if request.user.username in settings.ADMINS:
                meme = 0
            else:
                meme = models.Team.objects.filter(owner=request.user).count()

            if text[0] > 30:
                return render(request, 'app/text.html', { 'title':'Ошибка', 'text':'Какое-то слово(а) в вашем описании'
                                                                         ' больше 30 символов.' })
            elif bad:
                return  render(request, 'app/text.html', { 'title':'Ошибка', 'text':'Проверьте формат ссылки на группу в'
                                                                                    ' Steam. Например: http://steamcommunity.com/groups/potatogroup'})
            elif badword:
                return render(request, 'app/text.html', { 'title':'Ошибка', 'text':'В названии или тексте содержатся недопустимые слова ' + str(words) })

            elif meme >= 2:
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
                    need_awp=form.cleaned_data['need_awp'],
                    need_rif=form.cleaned_data['need_rif'],
                    need_sup=form.cleaned_data['need_sup'],
                    need_luk=form.cleaned_data['need_luk'],
                    need_frg=form.cleaned_data['need_frg'],
                    need_igl=form.cleaned_data['need_igl'],
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
        type = request.GET['type']
        if type == 'team':
            mod = models.Team.objects.filter(id=id, owner=request.user)
        elif type == 'player': #TODO: Player model
            mod = models.Team.objects.filter(id=id, owner=request.user)
        else:
            return render(request, 'app/text.html', {'title': 'Ошибка',
                                                     'text': 'Такой команды, игрока не существует либо она не принадлежит пользователю'})
        for i in mod:
            i.delete()
        return redirect('/myposts')
    except Exception:
        return render(request, 'app/text.html', {'title':'Ошибка', 'text':'Такой команды, игрока не существует либо она не принадлежит пользователю.'})
def update(request):
    try:
        id = int(request.GET['id'])
        type = request.GET['type']
        if type == 'team':
            mod = models.Team.objects.filter(id=id, owner=request.user)
        elif type == 'player': #TODO: Player model
            mod = models.Team.objects.filter(id=id, owner=request.user)
        else:
            return render(request, 'app/text.html', {'title': 'Ошибка',
                                                     'text': 'Такой команды, игрока не существует либо она не принадлежит пользователю'})
        for i in mod:
            if calendar.timegm(datetime.now().timetuple()) - calendar.timegm(i.registered.timetuple()) > 604800: # 7 days
                i.registered = datetime.now()
                i.save()
        return redirect('/myposts')
    except Exception:
        return render(request, 'app/text.html', {'title':'Ошибка', 'text':'Такой команды, игрока не существует либо она не принадлежит пользователю.'})
def crondis(request):
    try:
        kk = request.GET['kek']
    except Exception:
        return HttpResponse(
            '<html>\n<head><title>404 Not Found</title></head>\n<body bgcolor="white">\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx/1.10.0 (Ubuntu)</center>\n</body>\n</html>')

    if kk == settings.CRON_KEY:
        tdel = datetime.utcfromtimestamp(calendar.timegm(datetime.now().timetuple()) - 2629743) # 1 month
        mod = models.Team.objects.exclude(registered__gte=tdel).delete()#TODO: Player model
        return HttpResponse("Deleted "+str(mod[0])+' entries.')
    else:
        return HttpResponse('<html>\n<head><title>404 Not Found</title></head>\n<body bgcolor="white">\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx/1.10.0 (Ubuntu)</center>\n</body>\n</html>')
