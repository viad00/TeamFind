from django.http import HttpResponse
from django.conf import settings
from os import system



def push(request):
    try:
        uwsgi.reload()
    except Exception:
        pass
    system(settings.CODE_UPDATE_EXEC)
    return HttpResponse()
