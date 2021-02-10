from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from notes.views import topic_delete
from notes.models import Note, Topic

# Checks if user is redirected to login page if not logged in. If user is not
# logged in, she/he should not be able to delete anything.
class TopicTestsDeleteTopicUserNotLoggedIn(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='kalle', email='john@smith.com', password='123')
        self.user1 = User.objects.get(username="kalle")
        Topic.objects.create(
            subject='Subject1', description='Desc1', owner=self.user1)
        self.topic1 = Topic.objects.get(subject="Subject1");
        self.url = reverse('url_topic_delete', kwargs={'topic_id': self.topic1.pk})
        self.response = self.client.get(self.url)

    def test_topic_delete_status_code_user_not_logged_in(self):
        self.assertEquals(self.response.status_code, 302)

    def test_topic_delete_redirect_user_not_logged_in(self):
        url = reverse('login')
        self.assertRedirects(self.response, url)

    def test_topic_delete_check_topic_is_still_there(self):
        self.assertTrue(Topic.objects.filter(pk=self.topic1.pk).exists())

# Tests if the owner of the topic can delete it (should succeed).
class TopicTestsDeleteTopic(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='kalle', email='john@smith.com', password='123')
        User.objects.create_user(
            username='eila', email='eila@smith.com', password='456')
        self.user1 = User.objects.get(username="kalle")
        self.user2 = User.objects.get(username="eila")
        # kalle is the logged in user:
        self.client.login(username='kalle', password='123')
        Topic.objects.create(
            subject='Subject1', description='Desc1', owner=self.user1)
        Topic.objects.create(
            subject='Subject2', description='Desc2', owner=self.user2)
        self.topic1 = Topic.objects.get(subject="Subject1");
        self.topic2 = Topic.objects.get(subject="Subject2");
        self.url = reverse('url_topic_delete', kwargs={'topic_id': self.topic1.pk})
        self.response = self.client.get(self.url)

    def test_topic_delete_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # Note: the closing "/" in the parameter of the resolve method is needed!
    def test_topic_delete_url_resolves_correct_method(self):
        method_to_serve_url = resolve('/topics/1/delete/').func
        self.assertEquals(method_to_serve_url, topic_delete)

    def test_topic_delete_check_navigation_links(self):
        url_home = reverse('url_home')
        self.assertContains(self.response, 'href="{0}"'.format(url_home))

    def test_topic_delete_check_form_exists(self):
        self.assertContains(self.response,'<form ', 1)

    def test_topic_delete_check_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # Deletes the topic really (post request):
    def test_topic_delete_valid(self):
        response = self.client.post(self.url)

        # Tries to find the deleted topic in db:
        self.assertFalse(Topic.objects.filter(pk=self.topic1.pk).exists())

# Checks that a logged in user can not delete others' topics.
class TopicTestsDeleteTopic_Hacker(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='kalle', email='john@smith.com', password='123')
        User.objects.create_user(
            username='eila', email='eila@smith.com', password='456')
        self.user1 = User.objects.get(username="kalle")

        # eila is the logged in user:
        self.client.login(username='eila', password='456')
        # The topic owner is kalle:
        Topic.objects.create(
            subject='Subject1', description='Desc1', owner=self.user1)
        self.topic1 = Topic.objects.get(subject="Subject1");
        self.url = reverse('url_topic_delete', kwargs={'topic_id': self.topic1.pk})
        self.response = self.client.get(self.url)

    def test_topic_delete_by_hacker_redirect(self):
        # HttpResponseForbidden() Returns the 403 status code.
        self.assertEquals(self.response.status_code, 403)

    def test_topic_delete_valid_post_by_hacker(self):
        response = self.client.post(self.url)

        # The original should be in the db, too:
        self.assertTrue(Topic.objects.filter(pk=self.topic1.pk).exists())
