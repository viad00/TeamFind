"""
Definition of models.
"""
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

RANKS = (
        ('UN', 'Без ранга'),
        ('S1', 'Сильвер 1'),
        ('S2', 'Сильвер 2'),
        ('S3', 'Сильвер 3'),
        ('S4', 'Сильвер 4'),
        ('S5', 'Сильвер Элита'),
        ('S6', 'Сильвер Великий Магистр'),
        ('N1', 'Золотая Звезда 1'),
        ('N2', 'Золотая Звезда 2'),
        ('N3', 'Золотая Звезда 3'),
        ('N4', 'Золотая Звезда Магистр'),
        ('M1', 'Магистр Хранитель 1'),
        ('M2', 'Магистр Хранитель 2'),
        ('M3', 'Магистр Хранитель Элита'),
        ('M4', 'Заслуженный Магистр Хранитель'),
        ('L1', 'Легендарный Беркут'),
        ('L2', 'Легендарный Беркут Магистр'),
        ('SM', 'Великий Магистр Высшего Ранга'),
        ('GE', 'Всемирная Элита'),
    )

TYPES = (
        ('MM', 'Соревновательный'),
        ('PU', 'Competitive PUGs'),
        ('LE', 'Соревновательная Лига'),
        ('CA', 'Казуальный'),
    )

class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    founded = models.DateField
    description = models.TextField(max_length=2000, default='Капитан команды ещё не дал описание.')
    team_url = models.URLField
    min_rank = models.CharField(max_length=2, choices=RANKS, default='UN')
    max_rank = models.CharField(max_length=2, choices=RANKS, default='GE')
    types = MultiSelectField(choices=TYPES, default='CA')
