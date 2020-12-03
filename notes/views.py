from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from notes.forms import NewTopicForm, EditTopicForm
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

# Parameter "topic_id" is a keyword argument (kwarg) referring to the primary key
# (pk) of the object. We named "topic_id" in urls.py.
def topic_edit(request, topic_id):
    user = request.user
    if user.is_authenticated:
        topic = get_object_or_404(Topic, pk=topic_id)
        if topic.owner != user: # Important!
            return HttpResponseForbidden()
        else:
            if request.method == 'POST':
                form = EditTopicForm(request.POST)
                if form.is_valid():
                    return redirect('url_topics')
            else:
                form = EditTopicForm()
        return render(request, 'topic_edit.html', {'topic_form': form})
    else:
        return redirect('login')
