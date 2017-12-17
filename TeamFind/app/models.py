"""
Definition of models.
"""
import django
from django.contrib.auth.models import User
from django.db import models
from app import strings

# Create your models here.


# Описание модели команд
class Team(models.Model):
    name = models.CharField(max_length=18)
    owner = models.ForeignKey(User, default=None)
    registered = models.DateTimeField(default=django.utils.timezone.now)
    founded = models.DateField(default=django.utils.timezone.now)
    description = models.TextField(max_length=500, default='There are no description for team yet')
    team_url = models.URLField(default=None)
    image = models.URLField(default=None)
    min_rank = models.CharField(max_length=2, choices=strings.RANKS, default='UN')
    max_rank = models.CharField(max_length=2, choices=strings.RANKS, default='GE')
    is_mm = models.BooleanField(default=True)
    is_pu = models.BooleanField(default=True)
    is_le = models.BooleanField(default=True)
    is_ca = models.BooleanField(default=True)
    need_awp = models.BooleanField(default=True)
    need_luk = models.BooleanField(default=True)
    need_rif = models.BooleanField(default=True)
    need_igl = models.BooleanField(default=True)
    need_sup = models.BooleanField(default=True)
    need_frg = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)


class Player(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, default=None)
    registered = models.DateTimeField(default=django.utils.timezone.now)
    description = models.TextField(max_length=5000, default='There are no description yet')
    enabled = models.BooleanField(default=True)


class BadWords(models.Model):
    word = models.CharField(max_length=100)
