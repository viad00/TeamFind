"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase
from django.conf import settings

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Главная', 2, 200)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertContains(response, 'Contact', 2, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 'О сайте', 2, 200)

    def test_players(self):
        """Tests the about page."""
        response = self.client.get('/players')
        self.assertContains(response, 'Players', 1, 200)

    def test_teams(self):
        """Tests the about page."""
        response = self.client.get('/teams')
        self.assertContains(response, 'Teams', 1, 200)

    def test_teamd(self):
        """Tests the about page."""
        response = self.client.get('/teamd/?n=0&e=9')
        self.assertContains(response, 'Error', 0, 200)

    def test_updateinfo(self):
        """Tests the about page."""
        response = self.client.get('/updateinfo')
        self.assertContains(response, 'Ошибка', 1, 200)

    def test_myposts(self):
        """Tests the about page."""
        response = self.client.get('/myposts')
        self.assertContains(response, 'Ошибка', 1, 200)

    def test_delete(self):
        """Tests the about page."""
        response = self.client.get('/delete')
        self.assertContains(response, 'Ошибка', 1, 200)

    def test_update(self):
        """Tests the about page."""
        response = self.client.get('/update')
        self.assertContains(response, 'Ошибка', 1, 200)

    def test_crondis(self):
        """Tests the about page."""
        response = self.client.get('/crondis?kek=' + settings.CRON_KEY)
        self.assertContains(response, 'Deleted', 1, 200)

    def test_addteam(self):
        response = self.client.get('/addteam')
        self.assertContains(response, 'Добавить команду', 1, 200)