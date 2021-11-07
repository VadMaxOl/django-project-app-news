from django import forms
from .models import News, Comments


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'flag_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'style': 'width:490px; height: 20px'}),
            'content': forms.Textarea(attrs={'class': 'content-box', 'style': 'width:490px; height: 150px'}),
        }


class CommentsForm(forms.ModelForm):
    '''
    name = forms.CharField(max_length=500)
    text = forms.CharField(max_length=3000)
    '''
    class Meta:
        model = Comments
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'style': 'min-width:460px; height: 20px'}),
            'text': forms.Textarea(attrs={'class': 'content-box', 'style': 'min-width:460px; min-height: 100px'}),
        }


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
