from django.forms import ModelForm
from .models import Blog
from django import forms

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content', 'image','category' ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'text-bold rounded-full form-control w-50'}),
            'content': forms.Textarea(attrs={'class': 'form-control w-75'}),
            'image': forms.TextInput(attrs={'class': 'form-control rounded-full w-75'}),
        }