from django.contrib import admin
from app.models import Team, BadWords, Player

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'adm_url', 'description')
    def adm_url(self, obj):
        return '<a href="https://steamcommunity.com/gid/' + str(obj.team_url) + '" target="_blank">steam</a>'
    adm_url.allow_tags = True
    pass

class BadWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'word',)
    pass

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    pass

admin.site.register(Team, TeamAdmin)
admin.site.register(BadWords, BadWordsAdmin)
admin.site.register(Player, PlayerAdmin)
