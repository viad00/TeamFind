from django.http import HttpResponse
from django.conf import settings
from os import system



def push(request):
    system(settings.CODE_UPDATE_EXEC)
    try:
        import uwsgi
        uwsgi.reload()
    except Exception:
        pass
    return HttpResponse()
