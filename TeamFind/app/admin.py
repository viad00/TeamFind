from django.contrib import admin
from app.models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'adm_url', 'description')
    def adm_url(self, obj):
        return '<a href="https://steamcommunity.com/gid/' + str(obj.team_url) + '" target="_blank">steam</a>'
    adm_url.allow_tags = True
    pass

admin.site.register(Team, TeamAdmin)