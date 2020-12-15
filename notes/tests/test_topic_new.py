from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from notes.views import topic_new
from notes.models import Note, Topic

# Checks if user is redirected to login page if not logged in.
class TopicTestsNewTopicUserNotLoggedIn(TestCase):
    def setUp(self):
        self.url = reverse('url_topic_new')
        self.response = self.client.get(self.url)
        User.objects.create_user(
            username='kalle', email='john@smith.com', password='123')

    def test_topic_new_view_status_code_user_not_logged_in(self):
        self.assertEquals(self.response.status_code, 302)

    def test_topic_new_view_redirect_user_not_logged_in(self):
        url = reverse('login')
        self.assertRedirects(self.response, url)


class TopicTestsNewTopicUserLoggedIn(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='kalle', email='john@smith.com', password='123')
        User.objects.create_user(
            username='eila', email='eila@smith.com', password='456')
        self.user1 = User.objects.get(username="kalle")
        self.user2 = User.objects.get(username="eila")
        # kalle is the logged in user:
        self.client.login(username='kalle', password='123')
        self.url = reverse('url_topic_new')
        self.response = self.client.get(self.url)

    def test_topic_new_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_topic_new_url_resolves_correct_method(self):
        method_to_serve_url = resolve('/topics/new').func
        self.assertEquals(method_to_serve_url, topic_new)

    def test_topic_new_navigation_links(self):
        url_home = reverse('url_home')
        self.assertContains(self.response, 'href="{0}"'.format(url_home))

    def test_topic_new_view_form_exists(self):
        self.assertContains(self.response,'<form ', 1)

    def test_topic_new_check_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_topic_new_invalid_post_data(self):
        data = {}
        # Should not accept empty dictionary -> does not redirect.
        response = self.client.post(self.url, data)
        self.assertFalse(Topic.objects.exists())
        self.assertEquals(response.status_code, 200)

    def test_topic_new_invalid_post_data_empty_fields(self):
        data = {
            'subject':'',
            'description':'',
        }
        # Should not accept empty values -> does not redirect.
        response = self.client.post(self.url, data)
        self.assertFalse(Topic.objects.exists())
        self.assertEquals(response.status_code, 200)

    def test_topic_new_valid_post_data(self):
        data = {
            'subject': 'Some Good Title',
            'description': 'Some nice description'
        }
        response = self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
