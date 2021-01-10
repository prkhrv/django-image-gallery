from django import forms
from .models import Gallery
from taggit.forms import *


class ImageForm(forms.ModelForm):
    image = forms.FileField(label='Image') 
    tags = TagField()   
    class Meta:
        model = Gallery
        fields = ('image','tags')