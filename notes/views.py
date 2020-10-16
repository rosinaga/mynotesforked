from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Note, Topic

def home(request):
    alltopics = Topic.objects.all()
    return render(request, 'home.html',{'topics_for_home': alltopics})

# Handles both showing the form and saving the new topic:
def topic_new(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        desc = request.POST['description']
        user = User.objects.first()  # TODO: get the currently logged in user
        topic = Topic.objects.create(
            subject=subject,
            description=desc,
            owner=user
        )
        return redirect('url_topics')
    return render(request, 'topic_new.html')
