from django.shortcuts import render
from .models import Note, Topic

def home(request):
    alltopics = Topic.objects.all()
    return render(request, 'home.html',{'topics_for_home': alltopics})
