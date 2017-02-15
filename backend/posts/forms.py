from django.forms import ModelForm
from django import forms

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'url', 'body', 'post_type', 'post_level', 'post_price']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'markdown',
                                          'id': 'markdown'}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
            'post_level': forms.Select(attrs={'class': 'form-control'}),
            'post_price': forms.Select(attrs={'class': 'form-control'}),           
            # 'hubs': forms.ModelMultipleChoiceField(queryset=Hub.objects.all(), to_field_name="hubs"),
        }
