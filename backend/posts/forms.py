from django.forms import ModelForm
from django import forms

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'url', 'body', 'tags']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'markdown',
                                          'id': 'markdown'}),
            # 'hubs': forms.ModelMultipleChoiceField(queryset=Hub.objects.all(), to_field_name="hubs"),
        }
