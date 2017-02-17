from django.forms import ModelForm
from django import forms

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'url', 'body', 'post_type', 'post_level', 'post_price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title'}),
            'url': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Url'}),       
            'body': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Description. 200-500 words.'}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
            'post_level': forms.Select(attrs={'class': 'form-control'}),
            'post_price': forms.Select(attrs={'class': 'form-control'}),           
            # 'hubs': forms.ModelMultipleChoiceField(queryset=Hub.objects.all(), to_field_name="hubs"),
        }
