# class ModelCreateForm(forms.ModelForm):
    
#     class Meta:
#         model = ModelCreate
#         fields = ("title","body")
from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
