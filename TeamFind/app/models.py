"""
Definition of models.
"""
import django
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, default=None)
    founded = models.DateField(default=django.utils.timezone.now)
    description = models.TextField(max_length=2000, default='Капитан команды ещё не дал описание. Сообщите об этом ему')
    team_url = models.URLField(default=None)
    min_rank = models.CharField(max_length=2, choices=settings.RANKS, default='UN')
    max_rank = models.CharField(max_length=2, choices=settings.RANKS, default='GE')
    is_mm = models.BooleanField(default=True)
    is_pu = models.BooleanField(default=True)
    is_le = models.BooleanField(default=True)
    is_ca = models.BooleanField(default=True)
