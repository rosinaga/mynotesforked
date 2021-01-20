from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count
from notes.forms import NewTopicForm, EditTopicForm, NoteForm
from notes.models import Note, Topic

def home(request):
    # Smart this annotate:
    alltopics = Topic.objects.all().annotate(notes_number=Count('notes'))
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
        if topic.owner != user: # Important - others must not be able to edit!
            return HttpResponseForbidden() # Returns the 403 status code.
        else:
            if request.method == 'POST':
                # Instance=topic links the form to the current topic.
                form = EditTopicForm(request.POST, instance=topic)
                if form.is_valid():
                    topic.save()
                    return redirect('url_topics')
            else:
                # Returns the form with the current values:
                form = EditTopicForm(instance=topic)
        return render(request, 'topic_edit.html', {'topic_form': form})
    else:
        return redirect('login')

def topic_delete(request, topic_id):
    user = request.user
    if user.is_authenticated:
        topic = get_object_or_404(Topic, pk=topic_id)
        if topic.owner != user: # Important - others must not be able to delete!
            return HttpResponseForbidden()
        else:
            if request.method == 'POST':
                topic.delete()
                return redirect('url_topics')
        return render(request, 'topic_confirm_delete.html', {'topic': topic})
    else:
        return redirect('login')

def note_list(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    notes = Note.objects.filter(topic=topic)
    return render(request, 'note_list.html',{'topic':topic, 'notes': notes})

# Handles both showing the form and saving the new note:
def note_new(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user # Gives you the currently logged-in user.
    if user.is_authenticated:
        if request.method == 'POST':
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.owner = user
                note.topic = topic
                note.save()
                return redirect('url_note_list', topic_id=topic.pk)
        else:
            form = NoteForm()
        return render(request, 'note_new.html', {'topic':topic, 'note_form': form})
    else:
        return redirect('login')

def note_edit(request, topic_id, note_id):
    user = request.user
    if user.is_authenticated:
        topic = get_object_or_404(Topic, pk=topic_id)
        note = get_object_or_404(Note, pk=note_id)
        if note.owner != user: # Important - others must not be able to edit!
            return HttpResponseForbidden() # Returns the 403 status code.
        else:
            if request.method == 'POST':
                form = NoteForm(request.POST, instance=note)
                if form.is_valid():
                    note.save()
                    return redirect('url_note_list',topic_id=topic.pk )
            else:
                # Returns the form with the current values:
                form = NoteForm(instance=note)
        return render(request, 'note_edit.html',
            {'note':note,'topic':topic,'note_form': form})
    else:
        return redirect('login')

def note_delete(request, topic_id, note_id):
    user = request.user
    if user.is_authenticated:
        topic = get_object_or_404(Topic, pk=topic_id)
        note = get_object_or_404(Note, pk=note_id)
        if note.owner != user: # Important - others must not be able to delete!
            return HttpResponseForbidden()
        else:
            if request.method == 'POST':
                note.delete()
                return redirect('url_note_list',topic_id=topic.pk )
        return render(request, 'note_confirm_delete.html', {'note':note,'topic': topic})
    else:
        return redirect('login')
