from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from notes.forms import NewTopicForm
from notes.models import Note, Topic

def home(request):
    alltopics = Topic.objects.all()
    return render(request, 'home.html',{'topics_for_home': alltopics})

# Handles both showing the form and saving the new topic:
def topic_new(request):
    user = request.user # Gives you the currently logged-in user.
    if user.is_authenticated:
        if request.method == 'POST':
            form = NewTopicForm(request.POST)
            if form.is_valid():
                topic = form.save(commit=False)
                topic.owner = user
                topic.save()
                return redirect('url_topics')
        else:
            form = NewTopicForm()
        return render(request, 'topic_new.html', {'topic_form': form})
    else:
        return redirect('login')

def topic_edit(request):
    user = request.user # Gives you the currently logged-in user.
    topic = request.topic
    # Only topic owner can edit the topic:
    if user.is_authenticated and user == topic.owner:
        if request.method == 'POST':
            form = NewTopicForm(request.POST)
            if form.is_valid():
                topic = form.save(commit=False)
                topic.owner = user
                topic.save()
                return redirect('url_topics')
        else:
            form = NewTopicForm()
        return render(request, 'topic_new.html', {'topic_form': form})
    else:
        return redirect('login')
