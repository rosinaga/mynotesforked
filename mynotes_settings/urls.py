"""mynotes_settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from notes import views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='url_home'),
    path('topics/', views.home, name='url_topics'),
    path('topics/new', views.topic_new, name='url_topic_new'),
    path('topics/<int:topic_id>/edit/', views.topic_edit, name='url_topic_edit'),
    path('topics/<int:topic_id>/delete/', views.topic_delete, name='url_topic_delete'),

    path('topics/<int:topic_id>/notes', views.note_list, name='url_note_list'),
    path('topics/<int:topic_id>/notes/new', views.note_new, name='url_note_new'),
    path('topics/<int:topic_id>/notes/<int:note_id>/edit', \
        views.note_edit, name='url_note_edit'),
    path('topics/<int:topic_id>/notes/<int:note_id>/delete', \
        views.note_delete, name='url_note_delete'),

    # Accounts:===============================================
    path('signup/',accounts_views.signup,name='url_signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
