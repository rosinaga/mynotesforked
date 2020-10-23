from django import forms
from notes.models import Topic

class NewTopicForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(),
        max_length=500,
        help_text='The max length of the text is 500 characters.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'description']
