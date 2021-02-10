from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    subject = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='topics'
    )

class Note(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notes'
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='topics')
