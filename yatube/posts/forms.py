from django import forms
from .validators import validate_not_empty
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')



# class PostForm(forms.ModelForm):
#     text = forms.CharField(validators=[validate_not_empty])
#     group = forms.CharField()
#     fields = ()
    