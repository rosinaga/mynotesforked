from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from notes.views import home
from notes.models import Note, Topic

# Tests with user not logged in:
class HomeTestsNotLoggedIn(TestCase):
    def test_home_view_status_code(self):
        self.url = reverse('url_home')
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home(self):
        method_to_serve_url = resolve('/').func
        self.assertEquals(method_to_serve_url, home)

    def test_home_view_grid_elem_exist(self):
        self.url = reverse('url_home')
        self.response = self.client.get(self.url)
        self.assertContains(self.response,
            '<div class="grid">', 1)
