from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import News, Comments


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
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


class RegistrationUserForm(UserCreationForm):
    phone = forms.CharField(max_length=12, required=False, help_text='Номер телефона')
    city = forms.CharField(max_length=36, required=False, help_text='Город')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
