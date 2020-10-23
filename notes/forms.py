from django import forms
from notes.models import Topic

class NewTopicForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), max_length=500)

    class Meta:
        model = Topic
        fields = ['subject', 'description']
